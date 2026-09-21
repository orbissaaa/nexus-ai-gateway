from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from core.config import get_settings
from core.rotator import NoProviderAvailable, ProviderRequestError, Rotator

router = APIRouter(prefix="/v1")


def get_rotator(request: Request) -> Rotator:
    return request.app.state.rotator


def require_gateway_auth(authorization: str | None = Header(default=None)) -> None:
    configured_key = get_settings().gateway_api_key
    if not configured_key:
        return
    expected = f"Bearer {configured_key}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing gateway API key")


@router.post("/chat/completions", dependencies=[Depends(require_gateway_auth)])
async def chat_completions(payload: Dict[str, Any], rotator: Rotator = Depends(get_rotator)) -> JSONResponse:
    if not isinstance(payload.get("messages"), list) or not payload["messages"]:
        raise HTTPException(status_code=400, detail="messages must be a non-empty array")
    if payload.get("stream") is True:
        raise HTTPException(
            status_code=400,
            detail="Streaming is not enabled in this gateway build; omit stream or set it to false",
        )
    try:
        result = await rotator.complete(payload)
        return JSONResponse(content=result)
    except NoProviderAvailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ProviderRequestError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.get("/health")
async def health(rotator: Rotator = Depends(get_rotator)) -> Dict[str, Any]:
    return await rotator.health()
