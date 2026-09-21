"""Tool registry + echo tool [F-AG-016]."""

from __future__ import annotations

from langchain_core.tools import BaseTool

from astroassist.core.artifacts import ScientificValue
from astroassist.tools import default_registry
from astroassist.tools.echo import echo


def test_echo_returns_scientific_value() -> None:
    art = echo("hello")
    assert isinstance(art, ScientificValue)
    assert art.value.value == 5.0
    assert art.value.unit == ""
    assert art.provenance.method == "derived"
    assert art.provenance.tool == "echo@1"
    assert art.provenance.parameters["text"] == "hello"


def test_echo_registered() -> None:
    assert default_registry.has("echo")
    spec = default_registry.get("echo")
    assert spec.domain == "compute"
    assert spec.risk_class == "safe"
    assert isinstance(spec.tool, BaseTool)


def test_registry_exposes_tools() -> None:
    names = {t.name for t in default_registry.tools()}
    assert "echo" in names
    assert default_registry.by_domain("compute")


def test_cost_estimate() -> None:
    spec = default_registry.get("echo")
    est = spec.estimate(text="abcd")
    assert est["est_bytes"] == 4
    assert est["queries"] == 0
