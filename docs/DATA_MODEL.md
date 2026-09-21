# Data model

## Principles
- No physical number without a unit (Astropy `Quantity`); dimensionless is explicit.
- No artifact without provenance.
- Observed vs catalogued vs derived is a first-class distinction (`method`).
- Raw payloads live on disk; model context sees summaries.

## Provenance record (attached to every artifact)
```python
class Provenance(BaseModel):
    artifact_id: str                # art_<ulid>
    created_at: datetime
    method: Literal["catalog_measurement","observation","derived","literature","user_input","resolver","fit","plot","code"]
    source: str | None              # "Gaia DR3", "SIMBAD", "ADS", "local_rag", "astropy"
    source_version: str | None      # data release, service version, package version
    source_record_id: str | None    # e.g. Gaia source_id, bibcode, VizieR catalog id
    query_id: str | None            # QueryArtifact that produced it
    inputs: list[str]               # artifact ids consumed (lineage)
    tool: str | None                # tool name + version
    code_hash: str | None           # sha256 of code that produced it
    parameters: dict                # thresholds, radii, options
    citation_keys: list[str]        # bib keys
    quality_flags: dict
    warnings: list[str]
```

## Artifact kinds
| Kind | Payload | Notes |
|---|---|---|
| `ResolvedObject` | canonical_name, aliases, coordinate (ICRS deg + frame/epoch), object_type, spectral_type, resolver, resolver_id | consumed by all downstream agents |
| `ScientificValue` | value, unit, uncertainty (sym or asym), distribution?, limits | serialized via `units.py` |
| `CatalogTable` | QTable → Parquet + column metadata (unit, ucd, description), row_count, source catalog id | large tables paged from DuckDB |
| `ObservationList` | rows: mission, instrument, filter/band, exposure, obs id, products, proprietary flag, footprint | MAST/ESO/HEASARC |
| `LightCurve` | time (Time), flux (Quantity), flux_err, quality mask, cadence, sector/quarter | Parquet + metadata |
| `Spectrum` | wavelength/frequency, flux, uncertainty, resolution, frame | specutils-compatible |
| `Image` | FITS path, HDU index, WCS summary, shape, statistics | cutouts derived |
| `FitResult` | model, parameters (Quantity ± unc), covariance, goodness_of_fit, residuals ref, input ids | |
| `PlotArtifact` | spec (JSON), code, svg/png paths, data artifact ids, theme, version, parent id | edits create new versions |
| `LiteratureSet` | papers: bibcode, title, authors, year, journal, abstract, citation_count, doi, arxiv, origin (ADS/local) | |
| `CitationSet` | claim → citation keys | built by synthesis |
| `QueryArtifact` | source, protocol (TAP/HTTP/astroquery), query text (ADQL/URL/params), status, started/finished, runtime, row_count, bytes, raw_response path, error, retries | |
| `CodeArtifact` | code, kernel id, stdout, stderr, outputs (artifact ids), approved_by, approved_at | |
| `PlanArtifact` | DAG steps with inputs/outputs, estimates, approvals | |
| `JobArtifact` | kind, status, progress, elapsed, external job id, result artifact | |
| `TraceEntry` | step, agent, source, duration_ms, query_id, tokens/cost | |

## Serialization
- Pydantic models with custom JSON encoders for `Quantity` (`{"value":..,"unit":".."}`), `SkyCoord` (`{"ra_deg","dec_deg","frame","epoch"}`), `Time` (`{"iso","scale","format"}`).
- Tabular payloads: Parquet (Arrow) with column-level metadata; ECSV for Astropy round-trip; FITS/VOTable on export.
- Every artifact also has a `summary` (≤ 512 chars) for LLM context.

## Storage layers
| Layer | Technology | Holds |
|---|---|---|
| In-memory | QTable, Quantity, SkyCoord, Time | live analysis in kernel |
| Files | `~/.astroassist/workspaces/<ws>/artifacts/…` | Parquet, ECSV, FITS, SVG, PNG, raw responses |
| Artifact catalog | DuckDB `catalog.duckdb` | artifact index, column metadata, analytics over Parquet |
| Metadata & state | SQLite `workspace.db` + LangGraph checkpointer | workspace/session/thread/message/job tables, graph checkpoints |
| Cache | SQLite/DuckDB `cache.db` + files | query cache keyed by source+version+query+params+auth scope, TTL per source |
| Schemas | `~/.astroassist/schemas/<source>.duckdb` | TAP_SCHEMA mirror with timestamps |
| Credentials | OS keyring | tokens only |

## Workspace layout
```
~/.astroassist/
  config.toml
  workspaces/<ws_id>/
    workspace.db  catalog.duckdb  cache.db
    artifacts/<art_id>/ (payload files)
    raw/<query_id>.(json|xml|fits)
    figures/  data/  exports/
    kernel/   (kernel connection files, scratch)
  schemas/
  logs/
```

## Versioning and lineage
- Artifacts are immutable; edits (plot changes, reruns) create new artifacts with `parent_id`.
- Lineage graph = `provenance.inputs` edges; the export walks this graph to build the notebook in dependency order.
