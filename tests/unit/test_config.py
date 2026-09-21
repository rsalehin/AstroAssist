"""Config precedence tests: defaults < TOML < env [F-CORE-008]."""

from __future__ import annotations

from pathlib import Path

import pytest

from astroassist.core.config import Settings, load_settings


def test_zero_config_defaults() -> None:
    s = Settings()
    assert s.model_profile == "balanced"
    assert s.host == "127.0.0.1"
    assert s.port == 8765
    assert s.cache_mode == "online"


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ASTROASSIST_MODEL_PROFILE", "mock")
    monkeypatch.setenv("ASTROASSIST_PORT", "9999")
    s = load_settings(config_path=Path("does-not-exist.toml"))
    assert s.model_profile == "mock"
    assert s.port == 9999


def test_toml_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("ASTROASSIST_MODEL_PROFILE", "ASTROASSIST_PORT"):
        monkeypatch.delenv(var, raising=False)
    cfg = tmp_path / "config.toml"
    cfg.write_text('model_profile = "research"\nport = 9000\n', encoding="utf-8")
    s = load_settings(config_path=cfg)
    assert s.model_profile == "research"
    assert s.port == 9000


def test_env_beats_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = tmp_path / "config.toml"
    cfg.write_text('model_profile = "research"\n', encoding="utf-8")
    monkeypatch.setenv("ASTROASSIST_MODEL_PROFILE", "mock")
    s = load_settings(config_path=cfg)
    assert s.model_profile == "mock"


def test_data_dir_is_path() -> None:
    s = Settings()
    assert isinstance(s.data_dir, Path)
    assert s.workspaces_dir == s.data_dir / "workspaces"
