"""Echo tool [F-AG-016] — the M0 end-to-end stub.

Returns a provenance-bearing :class:`ScientificValue` (the character count of the input) so the
whole path tool -> artifact -> API -> UI card -> test can be exercised deterministically.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from astroassist.core.artifacts import ScientificValue
from astroassist.core.provenance import Provenance
from astroassist.core.units import QuantityValue
from astroassist.tools.registry import default_registry


class EchoInput(BaseModel):
    text: str = Field(description="Text to echo back.")


def echo(text: str) -> ScientificValue:
    return ScientificValue(
        summary=f"Echo of: {text}"[:512],
        provenance=Provenance(
            method="derived",
            source="astroassist",
            tool="echo@1",
            parameters={"text": text},
        ),
        value=QuantityValue(value=float(len(text)), unit=""),
    )


def _estimate(text: str = "") -> dict[str, Any]:
    return {"queries": 0, "est_rows": 0, "est_bytes": len(text), "est_seconds": 0}


echo_spec = default_registry.register(
    echo,
    name="echo",
    description="Echo the input text back as a ScientificValue (its character count).",
    args_schema=EchoInput,
    domain="compute",
    risk_class="safe",
    cost_estimator=_estimate,
)
