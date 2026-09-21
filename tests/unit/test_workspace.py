"""Workspace store + artifact catalog tests [F-WS-001][F-WS-002]."""

from __future__ import annotations

from pathlib import Path

import astropy.units as u

from astroassist.core.artifacts import ScientificValue
from astroassist.core.provenance import Provenance
from astroassist.core.units import QuantityValue
from astroassist.workspace.catalog import ArtifactCatalog
from astroassist.workspace.store import WorkspaceStore


def _value(summary: str = "distance = 4.965 pc") -> ScientificValue:
    return ScientificValue(
        summary=summary,
        provenance=Provenance(method="derived", source="astropy"),
        value=QuantityValue.from_quantity(4.965 * u.pc),
    )


def test_create_and_list_workspace(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    ws = store.create_workspace("AD Leo study")
    assert ws.id.startswith("ws_")
    assert [w.id for w in store.list_workspaces()] == [ws.id]
    assert store.get_workspace(ws.id) is not None


def test_thread_and_messages(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    ws = store.create_workspace("w")
    thread = store.create_thread(ws.id, title="chat")
    store.add_message(thread.id, "user", "hello")
    store.add_message(thread.id, "assistant", "hi")
    msgs = store.list_messages(thread.id)
    assert [m.role for m in msgs] == ["user", "assistant"]
    assert [m.content for m in msgs] == ["hello", "hi"]


def test_artifact_persisted_to_disk_and_reloaded(tmp_path: Path) -> None:
    store = WorkspaceStore(tmp_path)
    ws = store.create_workspace("w")
    thread = store.create_thread(ws.id)
    art = _value()
    store.add_artifact(ws.id, thread.id, art)

    on_disk = store.artifact_dir(ws.id, art.id) / "artifact.json"
    assert on_disk.exists()

    loaded = store.get_artifact(art.id)
    assert isinstance(loaded, ScientificValue)
    assert loaded.value.to_quantity().unit == u.pc
    assert [a.id for a in store.list_artifacts(ws.id)] == [art.id]


def test_duckdb_catalog_roundtrip(tmp_path: Path) -> None:
    catalog = ArtifactCatalog(tmp_path / "catalog.duckdb")
    catalog.register(
        artifact_id="art_1",
        workspace_id="ws_1",
        thread_id="thr_1",
        kind="ScientificValue",
        summary="x = 1",
        path="artifacts/art_1/artifact.json",
    )
    rows = catalog.list(workspace_id="ws_1")
    assert len(rows) == 1
    assert rows[0]["kind"] == "ScientificValue"
    assert catalog.get("art_1")["summary"] == "x = 1"
    catalog.close()
