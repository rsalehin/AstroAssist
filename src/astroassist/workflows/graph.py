"""LangGraph skeleton [F-AG-001].

M0 graph: ingest -> route (stub) -> execute (echo tool) -> synthesize. Tools return typed
artifacts (carried as dicts in state); the synthesis node produces the natural-language answer
via the active :class:`ModelProvider`. A SQLite checkpointer persists state per thread id.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from astroassist.core.artifacts import artifact_to_dict
from astroassist.core.models.base import ModelProvider
from astroassist.tools.echo import echo
from astroassist.workflows.state import ResearchState


def make_sqlite_checkpointer(path: Path | str) -> SqliteSaver:
    """A persistent SQLite checkpointer for graph state."""
    conn = sqlite3.connect(str(path), check_same_thread=False)
    return SqliteSaver(conn)


def build_graph(provider: ModelProvider, checkpointer: BaseCheckpointSaver | None = None) -> object:
    """Compile the M0 research graph for a given model provider."""

    def ingest(state: ResearchState) -> dict:
        text = state.get("input_text", "")
        return {
            "messages": [HumanMessage(content=text)],
            "trace": [{"step": "ingest", "agent": "ingest"}],
        }

    def route(state: ResearchState) -> dict:
        # M0 stub: deterministic intent. The cheap-model router lands in M1.
        return {"intent": "echo", "trace": [{"step": "route", "agent": "router"}]}

    def execute(state: ResearchState) -> dict:
        start = time.perf_counter()
        artifact = echo(state.get("input_text", ""))
        duration_ms = int((time.perf_counter() - start) * 1000)
        return {
            "artifacts": [artifact_to_dict(artifact)],
            "trace": [
                {"step": "execute", "agent": "compute", "tool": "echo", "duration_ms": duration_ms}
            ],
        }

    def synthesize(state: ResearchState) -> dict:
        model = provider.get_chat_model("synthesis")
        result = model.invoke(state.get("messages", []))
        text = str(result.content)
        return {
            "final_text": text,
            "messages": [AIMessage(content=text)],
            "trace": [{"step": "synthesize", "agent": "synthesis"}],
        }

    graph = StateGraph(ResearchState)
    graph.add_node("ingest", ingest)
    graph.add_node("route", route)
    graph.add_node("execute", execute)
    graph.add_node("synthesize", synthesize)
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "route")
    graph.add_edge("route", "execute")
    graph.add_edge("execute", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver())
