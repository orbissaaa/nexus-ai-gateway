from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Dict, List

import httpx

from .config import ProviderConfig
from .quota_tracker import QuotaTracker


class NoProviderAvailable(RuntimeError):
    pass


class ProviderRequestError(RuntimeError):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


class Rotator:
    def __init__(self, providers: List[ProviderConfig], tracker: QuotaTracker, timeout: float = 60.0) -> None:
        self.providers = providers
        self.tracker = tracker
        self.timeout = timeout
        self._cursor = 0
        self._cursor_lock = asyncio.Lock()

    async def _next_provider(self) -> ProviderConfig | None:
        if not self.providers:
            return None
        async with self._cursor_lock:
            total = len(self.providers)
            for offset in range(total):
                index = (self._cursor + offset) % total
                provider = self.providers[index]
                if await self.tracker.is_key_available(provider.key):
                    self._cursor = (index + 1) % total
                    return provider
        return None

    @staticmethod
    def _endpoint(provider: ProviderConfig) -> str:
        if provider.base_url.endswith("/chat/completions"):
            return provider.base_url
        return f"{provider.base_url}/chat/completions"

    @staticmethod
    def _headers(provider: ProviderConfig) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {provider.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def complete(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        attempted: list[str] = []
        last_error: str | None = None
        for _ in range(len(self.providers)):
            provider = await self._next_provider()
            if provider is None:
                break
            attempted.append(provider.name)
            upstream_payload = dict(payload)
            upstream_payload["model"] = provider.model
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self._endpoint(provider),
                        headers=self._headers(provider),
                        json=upstream_payload,
                    )
            except httpx.RequestError as exc:
                last_error = f"Provider {provider.name} request failed: {exc}"
                continue

            if response.status_code == 429:
                retry_after = response.headers.get("retry-after")
                cooldown = self.tracker.cooldown_seconds
                if retry_after and retry_after.isdigit():
                    cooldown = max(cooldown, int(retry_after))
                await self.tracker.mark_exhausted(provider.key, cooldown)
                last_error = f"Provider {provider.name} returned HTTP 429"
                continue

            if response.status_code >= 500:
                last_error = f"Provider {provider.name} returned HTTP {response.status_code}"
                continue

            if response.status_code >= 400:
                raise ProviderRequestError(
                    f"Provider {provider.name} rejected the request: {response.text[:500]}",
                    status_code=response.status_code,
                )

            try:
                return response.json()
            except ValueError as exc:
                raise ProviderRequestError("Provider returned invalid JSON") from exc

        if not attempted:
            raise NoProviderAvailable("No provider API keys are currently available")
        raise ProviderRequestError(
            last_error or "All configured providers failed after failover",
            status_code=502,
        )

    async def health(self) -> Dict[str, Any]:
        active = await self.tracker.active_count([provider.key for provider in self.providers])
        return {
            "status": "ok" if active else "degraded",
            "providers_configured": len(self.providers),
            "providers_active": active,
            "providers_exhausted": len(self.providers) - active,
        }
