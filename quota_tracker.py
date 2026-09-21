from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class ExhaustionRecord:
    exhausted_at: float
    retry_after: float


class QuotaTracker:
    def __init__(self, cooldown_seconds: int = 86400) -> None:
        self.cooldown_seconds = cooldown_seconds
        self._records: Dict[str, ExhaustionRecord] = {}
        self._lock = asyncio.Lock()

    async def mark_exhausted(self, key_id: str, cooldown_seconds: int | None = None) -> None:
        now = time.time()
        cooldown = float(cooldown_seconds or self.cooldown_seconds)
        async with self._lock:
            self._records[key_id] = ExhaustionRecord(
                exhausted_at=now,
                retry_after=now + cooldown,
            )

    async def is_key_available(self, key_id: str) -> bool:
        async with self._lock:
            record = self._records.get(key_id)
            if record is None:
                return True
            if time.time() >= record.retry_after:
                self._records.pop(key_id, None)
                return True
            return False

    async def seconds_until_available(self, key_id: str) -> int:
        async with self._lock:
            record = self._records.get(key_id)
            if record is None:
                return 0
            remaining = max(0.0, record.retry_after - time.time())
            if remaining == 0:
                self._records.pop(key_id, None)
            return int(remaining)

    async def active_count(self, key_ids: list[str]) -> int:
        count = 0
        for key_id in key_ids:
            if await self.is_key_available(key_id):
                count += 1
        return count
