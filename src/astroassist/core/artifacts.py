"""Typed scientific artifacts [F-CORE-003].

Every scientific output is one of these models, each carrying a :class:`Provenance`.
Physical numbers use the astropy wrappers from :mod:`astroassist.core.units`. Tabular and
binary payloads (Parquet/ECSV/FITS/SVG) live on disk and are referenced by path here; the
model context only ever sees the ``summary`` and structured metadata.

The kinds mirror docs/DATA_MODEL.md. :data:`AnyArtifact` is the discriminated union used for
(de)serialization across the API and workspace store.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, TypeAdapter

from astroassist.core.provenance import Provenance, new_artifact_id
from astroassist.core.units import QuantityValue, SkyCoordValue

# --- shared sub-models ------------------------------------------------------------------


class Uncertainty(BaseModel):
    """Symmetric or asymmetric uncertainty, each bound a unit-bearing quantity."""

    symmetric: QuantityValue | None = None
    lower: QuantityValue | None = None
    upper: QuantityValue | None = None


class ColumnMeta(BaseModel):
    name: str
    unit: str | None = None
    ucd: str | None = None
    description: str | None = None


class ObservationRow(BaseModel):
    mission: str
    instrument: str | None = None
    band: str | None = None
    exposure: QuantityValue | None = None
    obs_id: str | None = None
    products: list[str] = Field(default_factory=list)
    proprietary: bool = False
    footprint: str | None = None


class Paper(BaseModel):
    bibcode: str | None = None
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    journal: str | None = None
    abstract: str | None = None
    citation_count: int | None = None
    doi: str | None = None
    arxiv: str | None = None
    origin: Literal["ADS", "local", "arxiv"] = "ADS"


class FitParameter(BaseModel):
    name: str
    value: QuantityValue
    uncertainty: Uncertainty | None = None


class PlanStep(BaseModel):
    id: str
    agent: str
    tool: str | None = None
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    estimate: dict[str, Any] = Field(default_factory=dict)
    approved: bool | None = None


# --- base -------------------------------------------------------------------------------


class Artifact(BaseModel):
    """Base of every artifact kind. Subclasses fix the ``kind`` discriminator."""

    id: str = Field(default_factory=new_artifact_id)
    kind: str
    summary: str = Field(max_length=512)
    provenance: Provenance
    parent_id: str | None = None


# --- kinds ------------------------------------------------------------------------------


class ResolvedObject(Artifact):
    kind: Literal["ResolvedObject"] = "ResolvedObject"
    canonical_name: str
    aliases: list[str] = Field(default_factory=list)
    coordinate: SkyCoordValue
    object_type: str | None = None
    spectral_type: str | None = None
    resolver: str
    resolver_id: str | None = None


class ScientificValue(Artifact):
    kind: Literal["ScientificValue"] = "ScientificValue"
    value: QuantityValue
    uncertainty: Uncertainty | None = None
    distribution: str | None = None
    limits: dict[str, Any] | None = None


class CatalogTable(Artifact):
    kind: Literal["CatalogTable"] = "CatalogTable"
    parquet_path: str | None = None
    columns: list[ColumnMeta] = Field(default_factory=list)
    row_count: int = 0
    source_catalog_id: str | None = None


class ObservationListArtifact(Artifact):
    kind: Literal["ObservationList"] = "ObservationList"
    rows: list[ObservationRow] = Field(default_factory=list)


class LightCurve(Artifact):
    kind: Literal["LightCurve"] = "LightCurve"
    parquet_path: str | None = None
    cadence: QuantityValue | None = None
    sector: int | None = None
    quarter: int | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class Spectrum(Artifact):
    kind: Literal["Spectrum"] = "Spectrum"
    parquet_path: str | None = None
    frame: str | None = None
    resolution: QuantityValue | None = None


class Image(Artifact):
    kind: Literal["Image"] = "Image"
    fits_path: str | None = None
    hdu_index: int = 0
    wcs_summary: str | None = None
    shape: list[int] = Field(default_factory=list)
    statistics: dict[str, Any] = Field(default_factory=dict)


class FitResult(Artifact):
    kind: Literal["FitResult"] = "FitResult"
    model: str
    parameters: list[FitParameter] = Field(default_factory=list)
    goodness_of_fit: dict[str, Any] = Field(default_factory=dict)
    residuals_ref: str | None = None


class PlotArtifact(Artifact):
    kind: Literal["PlotArtifact"] = "PlotArtifact"
    spec: dict[str, Any] = Field(default_factory=dict)
    code: str | None = None
    svg_path: str | None = None
    png_path: str | None = None
    data_artifact_ids: list[str] = Field(default_factory=list)
    theme: str | None = None
    version: int = 1


class LiteratureSet(Artifact):
    kind: Literal["LiteratureSet"] = "LiteratureSet"
    papers: list[Paper] = Field(default_factory=list)


class CitationSet(Artifact):
    kind: Literal["CitationSet"] = "CitationSet"
    claims: dict[str, list[str]] = Field(default_factory=dict)


class QueryArtifact(Artifact):
    kind: Literal["QueryArtifact"] = "QueryArtifact"
    source: str
    protocol: Literal["TAP", "HTTP", "astroquery", "cone", "SIA", "SSA"] = "HTTP"
    query_text: str
    status: Literal["ok", "error", "pending", "cancelled"] = "pending"
    started_at: datetime | None = None
    finished_at: datetime | None = None
    runtime_ms: int | None = None
    row_count: int | None = None
    bytes: int | None = None
    raw_response_path: str | None = None
    error: str | None = None
    retries: int = 0


class CodeArtifact(Artifact):
    kind: Literal["CodeArtifact"] = "CodeArtifact"
    code: str
    kernel_id: str | None = None
    stdout: str | None = None
    stderr: str | None = None
    outputs: list[str] = Field(default_factory=list)
    approved_by: str | None = None
    approved_at: datetime | None = None


class PlanArtifact(Artifact):
    kind: Literal["PlanArtifact"] = "PlanArtifact"
    steps: list[PlanStep] = Field(default_factory=list)


class JobArtifact(Artifact):
    kind: Literal["JobArtifact"] = "JobArtifact"
    job_kind: str
    status: Literal["queued", "running", "done", "error", "cancelled"] = "queued"
    progress: float = 0.0
    elapsed_ms: int | None = None
    external_job_id: str | None = None
    result_artifact_id: str | None = None


# --- non-artifact record: research trace entry ------------------------------------------


class TraceEntry(BaseModel):
    """One research-trace step. An event-level record (streamed as a ``trace`` event),
    not a provenance-bearing artifact."""

    step: str
    agent: str | None = None
    source: str | None = None
    duration_ms: int | None = None
    query_id: str | None = None
    tokens: int | None = None
    cost: float | None = None


# --- discriminated union ----------------------------------------------------------------

AnyArtifact = Annotated[
    ResolvedObject
    | ScientificValue
    | CatalogTable
    | ObservationListArtifact
    | LightCurve
    | Spectrum
    | Image
    | FitResult
    | PlotArtifact
    | LiteratureSet
    | CitationSet
    | QueryArtifact
    | CodeArtifact
    | PlanArtifact
    | JobArtifact,
    Field(discriminator="kind"),
]

AnyArtifactAdapter: TypeAdapter[Any] = TypeAdapter(AnyArtifact)


def artifact_from_dict(data: dict[str, Any]) -> Artifact:
    """Deserialize any artifact dict into its concrete kind via the ``kind`` discriminator."""
    result: Artifact = AnyArtifactAdapter.validate_python(data)
    return result


def artifact_to_dict(artifact: Artifact) -> dict[str, Any]:
    """Serialize an artifact to a JSON-safe dict (astropy wrappers already primitive)."""
    return artifact.model_dump(mode="json")
