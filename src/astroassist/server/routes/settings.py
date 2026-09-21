"""Settings routes (read/update non-secret settings) [F-UI-018].

Credentials are never returned here; they are managed via the credential manager. M0 exposes the
non-secret runtime settings and echoes accepted updates for the active process.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from astroassist.server.context import AppContext
from astroassist.server.routes.deps import get_ctx

router = APIRouter(prefix="/api", tags=["settings"])


class SettingsPatch(BaseModel):
    model_profile: str | None = None
    cache_mode: str | None = None


def _public_settings(ctx: AppContext) -> dict[str, Any]:
    s = ctx.settings
    return {
        "model_profile": s.model_profile,
        "cache_mode": s.cache_mode,
        "host": s.host,
        "port": s.port,
        "langsmith_tracing": s.langsmith_tracing,
    }


@router.get("/settings")
def get_settings_route(ctx: AppContext = Depends(get_ctx)) -> dict[str, Any]:
    return _public_settings(ctx)


@router.put("/settings")
def put_settings_route(body: SettingsPatch, ctx: AppContext = Depends(get_ctx)) -> dict[str, Any]:
    if body.model_profile is not None:
        ctx.settings.model_profile = body.model_profile  # type: ignore[assignment]
    if body.cache_mode is not None:
        ctx.settings.cache_mode = body.cache_mode  # type: ignore[assignment]
    return _public_settings(ctx)
