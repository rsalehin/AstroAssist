"""FastAPI server + SSE echo round-trip [F-CORE-001]."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from astroassist.core.config import Settings
from astroassist.server.app import create_app


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    settings = Settings(model_profile="mock", data_dir=tmp_path)
    return TestClient(create_app(settings))


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["profile"] == "mock"


def test_bootstrap_and_settings(client: TestClient) -> None:
    r = client.get("/api/bootstrap")
    assert r.status_code == 200
    body = r.json()
    assert body["workspace_id"].startswith("ws_")
    assert body["thread_id"].startswith("thr_")
    assert client.get("/api/settings").json()["model_profile"] == "mock"


def _read_sse(client: TestClient, thread_id: str, text: str) -> list[dict]:
    events: list[dict] = []
    with client.stream("POST", f"/api/threads/{thread_id}/messages", json={"text": text}) as r:
        assert r.status_code == 200
        for line in r.iter_lines():
            if line.startswith("data:"):
                events.append(json.loads(line[len("data:") :].strip()))
    return events


def test_echo_message_streams_artifact(client: TestClient) -> None:
    thread_id = client.get("/api/bootstrap").json()["thread_id"]
    events = _read_sse(client, thread_id, "hello")
    types = [e["type"] for e in events]
    assert "artifact" in types
    assert types[-1] == "done"

    artifact_events = [e for e in events if e["type"] == "artifact"]
    art = artifact_events[0]["artifact"]
    assert art["kind"] == "ScientificValue"
    assert art["value"]["value"] == 5.0

    # artifact retrievable and persisted in the workspace
    got = client.get(f"/api/artifacts/{art['id']}")
    assert got.status_code == 200
    assert got.json()["kind"] == "ScientificValue"


def test_message_unknown_thread_404(client: TestClient) -> None:
    with client.stream("POST", "/api/threads/thr_nope/messages", json={"text": "x"}) as r:
        assert r.status_code == 404
