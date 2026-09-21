"""Mock model provider + fixtures CLI [F-EVAL-001]."""

from __future__ import annotations

from pathlib import Path

from langchain_core.messages import HumanMessage
from typer.testing import CliRunner

from astroassist.cli import app
from astroassist.core.config import Settings
from astroassist.core.models import build_provider
from astroassist.core.models.mock import MockModelProvider, MockResponse, MockScript

runner = CliRunner()


def test_default_script_synthesis() -> None:
    provider = MockModelProvider.default()
    model = provider.get_chat_model("synthesis")
    out = model.invoke([HumanMessage(content="hello")])
    assert "Echo" in str(out.content)


def test_response_matching_by_substring() -> None:
    script = MockScript(
        responses=[
            MockResponse(role="router", text="default-intent"),
            MockResponse(role="router", match="light curve", text="time_domain"),
        ]
    )
    assert script.response_for("router", "give me a light curve") == "time_domain"
    assert script.response_for("router", "who are you") == "default-intent"


def test_build_provider_returns_mock() -> None:
    provider = build_provider(Settings(model_profile="mock"))
    assert provider.name == "mock"


def test_script_from_yaml(tmp_path: Path) -> None:
    yaml_path = tmp_path / "scenario.yaml"
    yaml_path.write_text(
        "responses:\n  - role: synthesis\n    text: scripted answer\n",
        encoding="utf-8",
    )
    script = MockScript.from_yaml(yaml_path)
    assert script.response_for("synthesis", "anything") == "scripted answer"


def test_fixtures_cli_writes_ts(tmp_path: Path) -> None:
    out = tmp_path / "artifacts.ts"
    result = runner.invoke(app, ["eval", "fixtures", "--ts", "--out", str(out)])
    assert result.exit_code == 0, result.stdout
    content = out.read_text(encoding="utf-8")
    assert "export const scientificValue" in content
    assert '"kind": "ScientificValue"' in content
    assert "artifactFixtures" in content
