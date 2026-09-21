"""CredentialManager precedence: keyring > env > session [F-CORE-007]."""

from __future__ import annotations

import pytest

from astroassist.core.credentials import CredentialManager


def test_session_store() -> None:
    cm = CredentialManager(use_keyring=False)
    assert cm.get("ads") is None
    cm.set_session("ads", "sess-token")
    assert cm.get("ads") == "sess-token"


def test_env_beats_session(monkeypatch: pytest.MonkeyPatch) -> None:
    cm = CredentialManager(use_keyring=False)
    cm.set_session("ads", "sess-token")
    monkeypatch.setenv("ADS_DEV_KEY", "env-token")
    assert cm.get("ads") == "env-token"


def test_unknown_source_returns_none() -> None:
    cm = CredentialManager(use_keyring=False)
    assert cm.get("nonexistent") is None


def test_set_without_keyring_falls_back_to_session() -> None:
    cm = CredentialManager(use_keyring=False)
    cm.set("openai", "abc", persist=True)
    assert cm.get("openai") == "abc"


def test_repr_does_not_leak_tokens() -> None:
    cm = CredentialManager(use_keyring=False)
    cm.set_session("ads", "super-secret-token")
    assert "super-secret-token" not in repr(cm)
