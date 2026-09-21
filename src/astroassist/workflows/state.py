"""LangGraph state schema [F-AG-001].

Mirrors docs/AGENTS.md ``ResearchState``. ``artifacts``/``trace``/``errors`` use additive
reducers so parallel branches (M1) can contribute independently. Artifacts are carried as
JSON-safe dicts (the discriminated-union shape from :mod:`astroassist.core.artifacts`).
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class ResearchState(TypedDict, total=False):
    thread_id: str
    profile: str
    input_text: str
    intent: str
    messages: Annotated[list[Any], add_messages]
    resolved_objects: dict[str, str]
    plan: dict[str, Any] | None
    step_results: dict[str, list[str]]
    artifacts: Annotated[list[dict[str, Any]], operator.add]
    trace: Annotated[list[dict[str, Any]], operator.add]
    errors: Annotated[list[dict[str, Any]], operator.add]
    pending_interrupt: dict[str, Any] | None
    final_text: str
