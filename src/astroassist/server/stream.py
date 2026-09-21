"""SSE event mapping [F-AG-018].

Emits the streaming event schema from docs/ARCHITECTURE.md: ``trace``, ``artifact``, ``token``,
``interrupt``, ``done`` — each as an SSE ``data:`` line carrying a JSON object with a ``type``.
The M0 graph is fast and deterministic, so we run it and replay its trace/artifacts/answer as a
stream; true partial-artifact streaming (astream_events) lands with the M1 planner.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from typing import Any

from astroassist.core.artifacts import artifact_from_dict
from astroassist.server.context import AppContext


def _event(payload: dict[str, Any]) -> dict[str, str]:
    return {"data": json.dumps(payload)}


def _chunk_text(text: str, size: int = 24) -> Iterator[str]:
    for i in range(0, len(text), size):
        yield text[i : i + size]


async def run_message_stream(
    ctx: AppContext, workspace_id: str, thread_id: str, text: str
) -> AsyncIterator[dict[str, str]]:
    """Run the graph for one message and yield SSE events in order."""
    ctx.store.add_message(thread_id, "user", text)
    config = {"configurable": {"thread_id": thread_id}}
    state: dict[str, Any] = ctx.graph.invoke(  # type: ignore[attr-defined]
        {"input_text": text, "thread_id": thread_id}, config=config
    )

    for entry in state.get("trace", []):
        yield _event({"type": "trace", **entry})

    for art in state.get("artifacts", []):
        ctx.store.add_artifact(workspace_id, thread_id, artifact_from_dict(art))
        yield _event({"type": "artifact", "artifact": art})

    final = state.get("final_text", "")
    ctx.store.add_message(thread_id, "assistant", final)
    for piece in _chunk_text(final):
        yield _event({"type": "token", "text": piece})

    yield _event({"type": "done", "thread_id": thread_id})
