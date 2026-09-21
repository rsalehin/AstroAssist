"""Tests for id helpers and provenance serialization [F-CORE-003]."""

from __future__ import annotations

from astroassist.core.provenance import Provenance, new_artifact_id, new_id, new_query_id


def test_ids_are_prefixed_and_unique() -> None:
    a, b = new_artifact_id(), new_artifact_id()
    assert a.startswith("art_") and b.startswith("art_")
    assert a != b
    assert new_query_id().startswith("q_")
    assert new_id("plot").startswith("plot_")


def test_provenance_json_round_trip() -> None:
    p = Provenance(
        method="catalog_measurement",
        source="Gaia DR3",
        source_version="DR3",
        inputs=["art_1", "art_2"],
        parameters={"radius_arcsec": 5.0},
        citation_keys=["gaia2023"],
    )
    restored = Provenance.model_validate_json(p.model_dump_json())
    assert restored.source == "Gaia DR3"
    assert restored.inputs == ["art_1", "art_2"]
    assert restored.parameters["radius_arcsec"] == 5.0
    assert restored.artifact_id == p.artifact_id
