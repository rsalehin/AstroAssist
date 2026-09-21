"""Round-trip and provenance tests for typed artifacts [F-CORE-003]."""

from __future__ import annotations

import astropy.units as u
from astropy.coordinates import SkyCoord

from astroassist.core.artifacts import (
    QueryArtifact,
    ResolvedObject,
    ScientificValue,
    Uncertainty,
    artifact_from_dict,
    artifact_to_dict,
)
from astroassist.core.provenance import Provenance
from astroassist.core.units import QuantityValue, SkyCoordValue


def _prov(method: str = "derived") -> Provenance:
    return Provenance(method=method, source="astropy")  # type: ignore[arg-type]


def test_provenance_defaults() -> None:
    p = Provenance(method="derived")
    assert p.artifact_id.startswith("art_")
    assert p.created_at.tzinfo is not None
    assert p.inputs == []
    assert p.parameters == {}


def test_scientific_value_round_trip() -> None:
    sv = ScientificValue(
        summary="distance = 4.965 pc",
        provenance=_prov(),
        value=QuantityValue.from_quantity(4.965 * u.pc),
        uncertainty=Uncertainty(symmetric=QuantityValue.from_quantity(0.01 * u.pc)),
    )
    restored = artifact_from_dict(artifact_to_dict(sv))
    assert isinstance(restored, ScientificValue)
    assert restored.value.to_quantity().unit == u.pc
    assert restored.value.value == sv.value.value
    assert restored.uncertainty is not None
    assert restored.summary == "distance = 4.965 pc"


def test_resolved_object_round_trip() -> None:
    ro = ResolvedObject(
        summary="AD Leo",
        provenance=_prov("resolver"),
        canonical_name="AD Leo",
        aliases=["GJ 388", "V* AD Leo"],
        coordinate=SkyCoordValue.from_skycoord(SkyCoord(ra=154.9 * u.deg, dec=19.87 * u.deg)),
        object_type="Flare Star",
        resolver="SIMBAD",
    )
    restored = artifact_from_dict(artifact_to_dict(ro))
    assert isinstance(restored, ResolvedObject)
    assert restored.canonical_name == "AD Leo"
    assert "GJ 388" in restored.aliases
    assert restored.coordinate.to_skycoord().ra.deg == ro.coordinate.ra_deg


def test_query_artifact_round_trip() -> None:
    q = QueryArtifact(
        summary="SIMBAD resolve AD Leo",
        provenance=_prov("resolver"),
        source="SIMBAD",
        protocol="astroquery",
        query_text="query id AD Leo",
        status="ok",
        row_count=1,
    )
    restored = artifact_from_dict(artifact_to_dict(q))
    assert isinstance(restored, QueryArtifact)
    assert restored.source == "SIMBAD"
    assert restored.status == "ok"


def test_discriminator_selects_kind() -> None:
    payload = artifact_to_dict(
        ScientificValue(
            summary="x",
            provenance=_prov(),
            value=QuantityValue(value=1.0, unit=""),
        )
    )
    assert payload["kind"] == "ScientificValue"
    assert isinstance(artifact_from_dict(payload), ScientificValue)


def test_summary_length_capped() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ScientificValue(
            summary="x" * 513,
            provenance=_prov(),
            value=QuantityValue(value=1.0, unit=""),
        )
