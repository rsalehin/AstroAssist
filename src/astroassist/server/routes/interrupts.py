"""Interrupt resolution route [F-AG-013].

M0 acknowledges resolutions; the graph starts raising interrupts (and this route resumes them)
in M1 with the preflight and escape-hatch flows.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from astroassist.server.context import AppContext
from astroassist.server.routes.deps import get_ctx
from astroassist.workflows.interrupts import InterruptResolution

router = APIRouter(prefix="/api", tags=["interrupts"])


@router.post("/interrupts/{interrupt_id}/resolve")
def resolve_interrupt(
    interrupt_id: str, body: InterruptResolution, ctx: AppContext = Depends(get_ctx)
) -> dict[str, str]:
    return {"interrupt_id": interrupt_id, "action": body.action, "status": "acknowledged"}
