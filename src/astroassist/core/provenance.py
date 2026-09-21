"""Provenance record and id helpers [F-CORE-003].

Every artifact carries a :class:`Provenance`. A tool that returns a bare value with no
provenance is a bug (CLAUDE.md rule 2). ``method`` records the epistemic status of the
value: observed vs catalogued vs derived is a first-class distinction.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field
from ulid import ULID

Method = Literal[
    "catalog_measurement",
    "observation",
    "derived",
    "literature",
    "user_input",
    "resolver",
    "fit",
    "plot",
    "code",
]


def new_id(prefix: str) -> str:
    """Return a sortable, prefixed id, e.g. ``art_01J...`` (ULID)."""
    return f"{prefix}_{ULID()}"


def new_artifact_id() -> str:
    return new_id("art")


def new_query_id() -> str:
    return new_id("q")


def _utcnow() -> datetime:
    return datetime.now(tz=UTC)


class Provenance(BaseModel):
    """Lineage and epistemic metadata attached to every artifact."""

    artifact_id: str = Field(default_factory=new_artifact_id)
    created_at: datetime = Field(default_factory=_utcnow)
    method: Method
    source: str | None = None
    source_version: str | None = None
    source_record_id: str | None = None
    query_id: str | None = None
    inputs: list[str] = Field(default_factory=list)
    tool: str | None = None
    code_hash: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    citation_keys: list[str] = Field(default_factory=list)
    quality_flags: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
