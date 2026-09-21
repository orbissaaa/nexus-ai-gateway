import asyncio
import os

os.environ.pop("GATEWAY_API_KEY", None)
for index in range(1, 101):
    for suffix in ("NAME", "KEY", "MODEL", "BASE_URL"):
        os.environ.pop(f"PROVIDER_{index}_{suffix}", None)

from httpx import ASGITransport, AsyncClient
from core.quota_tracker import QuotaTracker
from main import create_app


async def main() -> None:
    tracker = QuotaTracker(cooldown_seconds=1)
    assert await tracker.is_key_available("demo")
    await tracker.mark_exhausted("demo")
    assert not await tracker.is_key_available("demo")
    await asyncio.sleep(1.1)
    assert await tracker.is_key_available("demo")

    async with AsyncClient(transport=ASGITransport(app=create_app()), base_url="http://test") as client:
        response = await client.get("/v1/health")
        assert response.status_code == 200, response.text
        assert response.json()["providers_configured"] == 0

    print("verification passed")


asyncio.run(main())
