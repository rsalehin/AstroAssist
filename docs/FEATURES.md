# Feature list

IDs are stable and referenced in commits, PRs, issues and tests. Milestones: M0 (skeleton), M1 (vertical slice), M2 (MVP sources), M3 (reproducibility + eval + alpha), M4+ (later). Status: ☐ planned · ◐ in progress · ☑ done.

## CORE — platform, config, credentials
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-CORE-001 | `astroassist serve` CLI starts backend and opens browser | M0 | ◐ |
| F-CORE-002 | Installable via `uv tool install` and `pip`; `environment.yml` for conda | M0 | ☑ |
| F-CORE-003 | Typed artifact base classes with mandatory provenance (Pydantic) | M0 | ☑ |
| F-CORE-004 | Unit-aware scientific types: Quantity, SkyCoord, Time, QTable throughout | M0 | ☑ |
| F-CORE-005 | `ModelProvider` protocol + adapters: Anthropic, OpenAI, OpenAI-compatible, Ollama, vLLM | M0 | ☑ |
| F-CORE-006 | Model profiles: economy / balanced / research / local; per-role model assignment (router, planner, synthesis) | M1 | ☐ |
| F-CORE-007 | `CredentialManager`: OS keyring → env var → session; never on disk in plaintext | M0 | ☑ |
| F-CORE-008 | Config file (`~/.astroassist/config.toml`) with sane zero-config defaults | M0 | ☑ |
| F-CORE-009 | Structured logging with secret redaction | M0 | ☑ |
| F-CORE-010 | Optional dependency groups / capability packs (timeseries, spectroscopy, imaging, dynamics, radio, interactive) | M1 | ☐ |
| F-CORE-011 | Capability limitation surfaced in UI when a pack or platform is unavailable | M2 | ☐ |
| F-CORE-012 | Docker compose deployment | M3 | ☐ |
| F-CORE-013 | Tauri desktop wrapper | M4 | ☐ |
| F-CORE-014 | Offline mode: local LLM + cached workspace analysis | M3 | ☐ |

## WS — workspace and persistence
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-WS-001 | Workspace / Session / Thread / Artifact model (SQLite metadata) | M0 | ☑ |
| F-WS-002 | Artifact store: files (Parquet/ECSV/FITS/SVG/PNG) + DuckDB catalog | M0 | ☑ |
| F-WS-003 | Per-workspace session object cache (resolved objects) | M1 | ☐ |
| F-WS-004 | Source-specific query cache with TTL policy; refresh / use-cached / offline modes | M1 | ☐ |
| F-WS-005 | Cache keyed by source + service version + query + params + auth scope | M1 | ☐ |
| F-WS-006 | Background job manager (async TAP jobs, downloads) with progress, cancel | M2 | ☐ |
| F-WS-007 | Persistent analysis kernel per workspace (jupyter_client): restart, clear, inspect variables, resource limits | M1 | ☐ |
| F-WS-008 | Workspace rename, duplicate, archive, delete | M3 | ☐ |
| F-WS-009 | Artifact referencing in chat (`@AD Leo`, `@TESS S45`) | M2 | ☐ |
| F-WS-010 | Bibliography accumulator per workspace (`references.bib`, `citations.json`) | M2 | ☐ |

## SRC — source connectors
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-SRC-000 | `SourcePlugin` interface: manifest, capabilities, auth, schema provider, tools, provenance adapter, rate policy | M0 | ☐ |
| F-SRC-001 | SIMBAD: resolve, aliases, basic data, bibliography | M1 | ☐ |
| F-SRC-002 | Sesame fallback resolver | M1 | ☐ |
| F-SRC-003 | Gaia archive: single-object, cone, ADQL (sync + async), TAP_SCHEMA sync | M1 | ☐ |
| F-SRC-004 | VizieR: catalog search, cone search, catalog metadata + reference paper, TAP | M2 | ☐ |
| F-SRC-005 | MAST: observation search, product listing, download, TESS/Kepler via lightkurve | M2 | ☐ |
| F-SRC-006 | ADS: search, abstracts, references/citations, bibcode → BibTeX; token via keyring | M2 | ☐ |
| F-SRC-007 | Local literature library (existing hybrid RAG: BGE-M3 + BM25 + SPECTER2 + citation graph) as a Literature source | M3 | ☐ |
| F-SRC-008 | NED: extragalactic object data, redshift, photometry | M4 | ☐ |
| F-SRC-009 | IRSA: 2MASS, WISE, ZTF | M4 | ☐ |
| F-SRC-010 | HEASARC: high-energy observation search | M4 | ☐ |
| F-SRC-011 | ESO archive | M4 | ☐ |
| F-SRC-012 | ALMA / NRAO archives | M4 | ☐ |
| F-SRC-013 | SDSS, NOIRLab Data Lab, Pan-STARRS | M4 | ☐ |
| F-SRC-014 | Time-domain: ZTF light curves, AAVSO, TNS | M4 | ☐ |
| F-SRC-015 | NASA Exoplanet Archive | M4 | ☐ |
| F-SRC-016 | Atomic/molecular: NIST ASD, VALD, CHIANTI, AtomDB, Splatalogue, CDMS/JPL, LAMDA | M4 | ☐ |
| F-SRC-017 | JPL Horizons, GWOSC, LAMBDA | M4 | ☐ |
| F-SRC-018 | Generic pyvo TAP/SIA/SSA/Cone connector for any IVOA service | M3 | ☐ |
| F-SRC-019 | Schema registry: local mirror of TAP_SCHEMA per service with timestamps and refresh | M1 | ☐ |
| F-SRC-020 | Per-connector `RatePolicy` (concurrency, rps, burst, retries, retry-after), backoff + jitter, circuit breaker, request dedup | M1 | ☐ |
| F-SRC-021 | Capability-aware fallback with explicit "not retrieved" report | M2 | ☐ |

## Q — query semantics
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-Q-001 | Object resolver runs on every new identifier; session cache first | M1 | ☐ |
| F-Q-002 | Coordinate input in all common forms (decimal, sexagesimal, Galactic, SkyCoord string); normalized to ICRS deg with frame/epoch metadata | M1 | ☐ |
| F-Q-003 | Source-selection policy: primary measurement source + context sources per question type | M1 | ☐ |
| F-Q-004 | Source disagreement detection and side-by-side display | M2 | ☐ |
| F-Q-005 | Risk-based confirmation: thresholds on radius, MAXREC, estimated rows/bytes, async duration, code exec, proprietary data, FS writes | M1 | ☐ |
| F-Q-006 | Preflight estimate: "N external queries, ~X MB" | M2 | ☐ |
| F-Q-007 | Generated ADQL/API call visible; copy; edit-and-rerun | M1 | ☐ |
| F-Q-008 | Schema-aware ADQL self-correction: max 2 autonomous retries then surface error with suggestion | M1 | ☐ |
| F-Q-009 | Raw response retained and viewable per query | M1 | ☐ |
| F-Q-010 | Unit conversion on request via Astropy (`in light-years`) | M1 | ☐ |

## TOOL — computation tools (curated, deterministic)
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-TOOL-001 | `convert_units` | M1 | ☐ |
| F-TOOL-002 | `coordinate_transform` (ICRS/Galactic/FK5/ecliptic, epoch propagation) | M1 | ☐ |
| F-TOOL-003 | `distance_from_parallax` (naive + optional probabilistic) | M1 | ☐ |
| F-TOOL-004 | `tangential_velocity`, `space_velocity (UVW)` | M1 | ☐ |
| F-TOOL-005 | `crossmatch` (Astropy match_to_catalog_sky) | M2 | ☐ |
| F-TOOL-006 | `sigma_clip`, `bin`, `detrend`, `normalize` | M2 | ☐ |
| F-TOOL-007 | `lomb_scargle`, `bls`, `phase_fold` | M2 | ☐ |
| F-TOOL-008 | `flare_detect` (threshold + simple template) | M2 | ☐ |
| F-TOOL-009 | Fit family → `FitResult`: linear/nonlinear LSQ, Gaussian, blackbody, power law, polynomial continuum, robust regression | M2 | ☐ |
| F-TOOL-010 | `build_sed` from multi-catalog photometry with filter zero-points | M3 | ☐ |
| F-TOOL-011 | Observation planning: visibility, airmass, alt/az, twilight, moon separation, hour angle, best window (astroplan) | M2 | ☐ |
| F-TOOL-012 | FITS: open, HDU list, header, statistics, cutout, WCS | M2 | ☐ |
| F-TOOL-013 | `absolute_magnitude`, `luminosity`, `color_index`, extinction helpers | M2 | ☐ |
| F-TOOL-014 | Cosmology calculators (astropy.cosmology) | M3 | ☐ |
| F-TOOL-015 | Python escape hatch: LLM proposes code → HITL approve/edit/cancel → run in kernel → `CodeArtifact` | M1 | ☐ |
| F-TOOL-016 | MCMC / nested sampling (emcee, dynesty) extra | M4 | ☐ |
| F-TOOL-017 | Photometry, source extraction, reprojection, mosaics (photutils/reproject) | M4 | ☐ |
| F-TOOL-018 | Spectroscopy tools (specutils): line ID with NIST, continuum, equivalent width | M4 | ☐ |
| F-TOOL-019 | RM synthesis / Faraday spectrum tools | M4 | ☐ |

## VIS — visualization
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-VIS-001 | Plot spec (declarative JSON) → matplotlib code → SVG/PNG; `PlotArtifact` carries data + code + spec | M1 | ☐ |
| F-VIS-002 | House style: colorblind-safe palette, units on axes, sensible error bars, vector export; `plot_theme.toml` | M1 | ☐ |
| F-VIS-003 | Natural-language plot editing modifies the spec, regenerates code | M2 | ☐ |
| F-VIS-004 | Typed plot tools: light curve, phase-folded LC, periodogram, HR/CMD, SED, spectrum, finder chart, sky map, image+WCS, corner, RV curve | M2–M3 | ☐ |
| F-VIS-005 | Interactive toggle (Plotly) for exploratory plots | M3 | ☐ |
| F-VIS-006 | Aladin Lite panel: surveys, Gaia overlay, catalog rows, footprints | M2 | ☐ |
| F-VIS-007 | Plot export: SVG, PNG, PDF + data + code | M2 | ☐ |
| F-VIS-008 | Show-code / regenerate on every plot card | M1 | ☐ |

## AG — agents and orchestration
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-AG-001 | LangGraph state schema with typed artifacts; SQLite checkpointer | M0 | ☑ |
| F-AG-002 | Intent router (cheap model) | M1 | ☐ |
| F-AG-003 | Planner producing explicit workflow DAG (parallel branches) | M1 | ☐ |
| F-AG-004 | Supervisor / replanner on step failure | M2 | ☐ |
| F-AG-005 | Object & Catalog Agent (SIMBAD, Gaia, VizieR, NED) | M1 | ☐ |
| F-AG-006 | Compute Agent (curated tools + escape hatch) | M1 | ☐ |
| F-AG-007 | Visualization Agent | M1 | ☐ |
| F-AG-008 | Observation Agent (MAST, later ESO/HEASARC/ALMA) | M2 | ☐ |
| F-AG-009 | Literature Agent (ADS, local RAG) | M2 | ☐ |
| F-AG-010 | Time-Domain Agent (lightkurve, later ZTF/AAVSO) | M2 | ☐ |
| F-AG-011 | Spectroscopy Agent (NIST, VALD, specutils) | M4 | ☐ |
| F-AG-012 | Synthesis node: cites artifact IDs, never invents numbers | M1 | ☐ |
| F-AG-013 | HITL interrupts: expensive query, large download, proprietary data, generated code, overwrite/delete, external export, high-impact ambiguous assumption | M1 | ◐ |
| F-AG-014 | Research Trace exposed to user (step, source, duration) | M2 | ☐ |
| F-AG-015 | LangSmith tracing (opt-in, redacted) | M0 | ☐ |
| F-AG-016 | Tool registry with typed schemas auto-exposed to agents | M0 | ☑ |
| F-AG-017 | Token/cost display per run (optional) | M3 | ☐ |
| F-AG-018 | Streaming of partial artifacts to UI | M1 | ☐ |

## UI — workbench
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-UI-001 | Three-pane workbench: workspace rail / chat / artifact viewer; bottom trace & jobs bar | M1 | ☐ |
| F-UI-002 | Chat with streaming, markdown + inline artifact cards | M1 | ☐ |
| F-UI-003 | Object card | M1 | ☐ |
| F-UI-004 | Scientific value card (value ± unc unit, source, derivation) | M1 | ☐ |
| F-UI-005 | Table viewer: units, metadata, sort/filter, export | M1 | ☐ |
| F-UI-006 | Query card: source, ADQL/API, status, runtime, edit-and-rerun | M1 | ☐ |
| F-UI-007 | Plot card: image, show code, data, regenerate, export | M1 | ☐ |
| F-UI-008 | Paper card (ADS) and Citation card | M2 | ☐ |
| F-UI-009 | Observation card (mission, instrument, band, exposure, download) | M2 | ☐ |
| F-UI-010 | FITS viewer with WCS axes and source overlay | M2 | ☐ |
| F-UI-011 | Aladin Lite panel | M2 | ☐ |
| F-UI-012 | Code viewer/editor for escape-hatch approvals | M1 | ☐ |
| F-UI-013 | HITL approval dialogs | M1 | ☐ |
| F-UI-014 | Jobs panel (running/queued/done; cancel) | M2 | ☐ |
| F-UI-015 | Research Trace panel | M2 | ☐ |
| F-UI-016 | Dark (default) + light themes, WCAG-AA contrast, keyboard focus | M1 | ☐ |
| F-UI-017 | Command palette (Ctrl/Cmd+K), Ctrl/Cmd+Enter, slash commands `/resolve /query /cone /plot /fit /cite /export` | M2 | ☐ |
| F-UI-018 | Settings: models, profiles, credentials, thresholds, cache, theme | M1 | ☐ |
| F-UI-019 | Source-disagreement banner | M2 | ☐ |
| F-UI-020 | Capability-limitation and fallback notices | M2 | ☐ |
| F-UI-021 | Desktop-only responsive floor (≥1280 px); read-only mobile later | M1 | ☐ |

## REPRO — reproducibility and export
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-REPRO-001 | Every action recorded as typed action + inputs + tool/code + output + provenance | M0 | ☐ |
| F-REPRO-002 | Table export: FITS, ECSV, VOTable, CSV, Parquet, LaTeX | M2 | ☐ |
| F-REPRO-003 | Research bundle export: notebook, script, lockfile, queries/, data/, figures/, references.bib, provenance.json, README | M3 | ☐ |
| F-REPRO-004 | Bundle re-execution check (bundle runs standalone) | M3 | ☐ |
| F-REPRO-005 | Session → Jupyter notebook incremental sync | M4 | ☐ |

## EVAL — testing and evaluation
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-EVAL-001 | Recorded-fixture unit tests for every connector and tool | M1 | ◐ |
| F-EVAL-002 | Live contract tests (nightly / manual) | M1 | ☐ |
| F-EVAL-003 | Astronomy benchmark (100–300 questions) with deterministic evaluators | M3 | ☐ |
| F-EVAL-004 | Agent-quality metrics (source selection, tool correctness, provenance completeness, trajectory efficiency, …) in LangSmith | M3 | ☐ |
| F-EVAL-005 | CI: lint, type-check, unit tests on 3.11/3.12/3.13 × Linux/macOS/Windows | M0 | ☐ |

## COMM — community and repo hygiene
| ID | Feature | Milestone | Status |
|---|---|---|---|
| F-COMM-001 | LICENSE (BSD-3), CITATION.cff, codemeta.json, CONTRIBUTING, CODE_OF_CONDUCT | M0 | ☐ |
| F-COMM-002 | Issue/PR templates, good-first-issue labels | M0 | ☐ |
| F-COMM-003 | Connector template + `/new-connector` command | M1 | ☐ |
| F-COMM-004 | Docs site (mkdocs-material) | M3 | ☐ |
| F-COMM-005 | JOSS-ready structure (tests, docs, examples, citation metadata, releases) | M3 | ☐ |
