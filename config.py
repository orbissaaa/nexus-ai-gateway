from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    key: str
    model: str
    base_url: str


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    request_timeout: float
    cooldown_seconds: int
    gateway_api_key: str | None
    providers: List[ProviderConfig]


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _load_providers() -> List[ProviderConfig]:
    providers: List[ProviderConfig] = []
    for index in range(1, 101):
        prefix = f"PROVIDER_{index}_"
        name = _clean(os.getenv(f"{prefix}NAME"))
        key = _clean(os.getenv(f"{prefix}KEY"))
        model = _clean(os.getenv(f"{prefix}MODEL"))
        base_url = _clean(os.getenv(f"{prefix}BASE_URL")) or "https://api.openai.com/v1"
        if not name and not key and not model and not os.getenv(f"{prefix}BASE_URL"):
            continue
        if not name or not key or not model:
            raise ValueError(
                f"Incomplete provider configuration at index {index}. "
                f"NAME, KEY, and MODEL are required."
            )
        providers.append(
            ProviderConfig(
                name=name.lower(),
                key=key,
                model=model.lower(),
                base_url=base_url.rstrip("/"),
            )
        )
    return providers


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        host=_clean(os.getenv("HOST")) or "0.0.0.0",
        port=int(_clean(os.getenv("PORT")) or "8000"),
        request_timeout=float(_clean(os.getenv("REQUEST_TIMEOUT")) or "60"),
        cooldown_seconds=int(_clean(os.getenv("COOLDOWN_SECONDS")) or "86400"),
        gateway_api_key=_clean(os.getenv("GATEWAY_API_KEY")) or None,
        providers=_load_providers(),
    )
