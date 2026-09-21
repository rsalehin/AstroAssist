"""LangGraph echo skeleton + checkpointing [F-AG-001][F-AG-013]."""

from __future__ import annotations

from pathlib import Path

from astroassist.core.models.mock import MockModelProvider
from astroassist.workflows.graph import build_graph, make_sqlite_checkpointer
from astroassist.workflows.interrupts import (
    InterruptPayload,
    large_query_interrupt,
    run_code_interrupt,
)


def test_echo_flow_produces_artifact_and_answer() -> None:
    graph = build_graph(MockModelProvider.default())
    config = {"configurable": {"thread_id": "t1"}}
    out = graph.invoke({"input_text": "hello", "thread_id": "t1"}, config=config)

    assert len(out["artifacts"]) == 1
    art = out["artifacts"][0]
    assert art["kind"] == "ScientificValue"
    assert art["value"]["value"] == 5.0
    assert "Echo" in out["final_text"]
    steps = [t["step"] for t in out["trace"]]
    assert steps == ["ingest", "route", "execute", "synthesize"]


def test_checkpoint_persisted(tmp_path: Path) -> None:
    checkpointer = make_sqlite_checkpointer(tmp_path / "checkpoints.db")
    graph = build_graph(MockModelProvider.default(), checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "abc"}}
    graph.invoke({"input_text": "hi", "thread_id": "abc"}, config=config)

    snapshot = graph.get_state(config)
    assert snapshot.values["artifacts"][0]["kind"] == "ScientificValue"
    assert snapshot.values["final_text"]


def test_interrupt_payloads() -> None:
    rc = run_code_interrupt(code="print(1)", why="compute distance")
    assert rc.reason == "run_code"
    assert rc.payload["code"] == "print(1)"
    assert rc.interrupt_id.startswith("int_")

    lq = large_query_interrupt(source="Gaia", query_text="SELECT *", est_rows=1_000_000)
    assert lq.reason == "large_query"
    assert lq.payload["est_rows"] == 1_000_000
    assert isinstance(lq, InterruptPayload)
