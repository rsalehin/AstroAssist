"""Artifact routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from astroassist.core.artifacts import artifact_to_dict
from astroassist.server.context import AppContext
from astroassist.server.routes.deps import get_ctx

router = APIRouter(prefix="/api", tags=["artifacts"])


@router.get("/artifacts/{artifact_id}")
def get_artifact(artifact_id: str, ctx: AppContext = Depends(get_ctx)) -> dict[str, Any]:
    art = ctx.store.get_artifact(artifact_id)
    if art is None:
        raise HTTPException(status_code=404, detail="artifact not found")
    return artifact_to_dict(art)
