"""Human-in-the-loop interrupt payloads [F-AG-013].

Every risky action pauses the graph with a typed payload the UI renders as an approval dialog.
M0 defines the schema and the ``run_code`` / ``large_query`` payloads; the graph starts issuing
them in M1 (preflight + escape hatch).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from astroassist.core.provenance import new_id

InterruptReason = Literal[
    "large_query",
    "large_download",
    "proprietary_data",
    "run_code",
    "overwrite_delete",
    "external_export",
    "scientific_assumption",
]


class RunCodePayload(BaseModel):
    code: str
    language: str = "python"
    kernel_id: str | None = None
    why: str | None = None


class LargeQueryPayload(BaseModel):
    source: str
    query_text: str
    est_rows: int | None = None
    est_bytes: int | None = None
    est_seconds: float | None = None


class InterruptPayload(BaseModel):
    interrupt_id: str = Field(default_factory=lambda: new_id("int"))
    reason: InterruptReason
    payload: dict[str, Any] = Field(default_factory=dict)


def run_code_interrupt(
    code: str, why: str | None = None, kernel_id: str | None = None
) -> InterruptPayload:
    return InterruptPayload(
        reason="run_code",
        payload=RunCodePayload(code=code, why=why, kernel_id=kernel_id).model_dump(),
    )


def large_query_interrupt(
    source: str,
    query_text: str,
    est_rows: int | None = None,
    est_bytes: int | None = None,
    est_seconds: float | None = None,
) -> InterruptPayload:
    return InterruptPayload(
        reason="large_query",
        payload=LargeQueryPayload(
            source=source,
            query_text=query_text,
            est_rows=est_rows,
            est_bytes=est_bytes,
            est_seconds=est_seconds,
        ).model_dump(),
    )


class InterruptResolution(BaseModel):
    """The user's decision on an interrupt (POST /api/interrupts/{id}/resolve)."""

    action: Literal["approve", "edit", "cancel"]
    edited_payload: dict[str, Any] | None = None
