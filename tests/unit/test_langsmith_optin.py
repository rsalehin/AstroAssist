"""LangSmith tracing is opt-in and env-driven [F-AG-015]."""

from __future__ import annotations

import pytest

from astroassist.core.config import Settings, apply_langsmith_env


def test_tracing_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    assert apply_langsmith_env(Settings(langsmith_tracing=False)) is False
    assert "LANGSMITH_TRACING" not in __import__("os").environ


def test_tracing_enabled_sets_env(monkeypatch: pytest.MonkeyPatch) -> None:
    import os

    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_PROJECT", raising=False)
    enabled = apply_langsmith_env(
        Settings(langsmith_tracing=True, langsmith_project="astroassist-test")
    )
    assert enabled is True
    assert os.environ["LANGSMITH_TRACING"] == "true"
    assert os.environ["LANGSMITH_PROJECT"] == "astroassist-test"
