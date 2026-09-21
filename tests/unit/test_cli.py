"""CLI smoke tests: the entry point exposes `version` and `serve` [F-CORE-001]."""

from __future__ import annotations

from typer.testing import CliRunner

from astroassist import __version__
from astroassist.cli import app

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_help_lists_serve() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "serve" in result.stdout
