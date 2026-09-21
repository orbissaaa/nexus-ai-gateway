from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from api.routes import router
from core.config import get_settings
from core.quota_tracker import QuotaTracker
from core.rotator import Rotator


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Universal Multi-Provider AI Gateway",
        version="1.0.0",
        description="OpenAI-compatible gateway for authorized multi-provider API keys.",
    )
    app.state.rotator = Rotator(
        providers=settings.providers,
        tracker=QuotaTracker(settings.cooldown_seconds),
        timeout=settings.request_timeout,
    )
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=False)
