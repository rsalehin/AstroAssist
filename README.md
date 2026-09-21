# AstroAssist

**An open-source research workbench for astronomers: natural language in, provenance-tracked science out.**

AstroAssist is a locally-run, multi-agent research assistant for astrophysics. You ask questions in plain language ("What is the distance to AD Leo? Find its TESS light curves and flag flares above 5σ"); AstroAssist resolves the object, queries the right archives (SIMBAD, Gaia, VizieR, MAST, ADS, …), runs unit-aware Astropy calculations, renders publication-quality plots, and returns **typed artifacts** where every number carries its unit, uncertainty, source, query and citation.

It is a *research* tool, not a chatbot: correctness → provenance → reproducibility → speed → aesthetics, in that order.

> Status: **pre-alpha, design phase**. The repository currently contains the full product specification and an implementation plan. Code is being built milestone by milestone (see [docs/ROADMAP.md](docs/ROADMAP.md)).

## Day-one story

> "Investigate AD Leo. Resolve the object, retrieve the best current astrometry and stellar properties, calculate distance and tangential velocity, find TESS observations, display a light curve, identify significant flares, find recent papers on its magnetic activity, and produce a research summary in which every number, plot, query and citation can be inspected and reproduced."

## Planned quick start

```bash
uv tool install astroassist        # or: pip install astroassist
astroassist serve                  # starts local FastAPI backend + opens browser workbench
```

Public archives work with zero configuration. Only sources that require tokens (ADS, proprietary MAST/ESO data) prompt for credentials, stored in your OS keyring.

## Key ideas

- **Workbench, not chat** — chat panel + persistent workspace rail (objects, tables, plots, papers, jobs) + artifact viewer (tables, plots, FITS, Aladin Lite, queries, code).
- **Typed artifacts, never free text** — `ResolvedObject`, `ScientificValue`, `CatalogTable`, `LightCurve`, `FitResult`, `PlotArtifact`, `CitationSet`, …
- **Provenance is mandatory** — every scientific value: value + unit + uncertainty + source + query id + retrieval time + method + lineage.
- **Agents are reasoning roles; sources are tools** — Object & Catalog, Observation, Literature, Time-Domain, Spectroscopy, Compute, Visualization agents; orchestrated with LangGraph, traced with LangSmith.
- **Every query and every line of code is inspectable** — View ADQL, edit and rerun, export session as a runnable notebook + data + `references.bib`.
- **Curated deterministic tools first; approved Python escape hatch second.**

## Documentation map

| Doc | What it is |
|---|---|
| [docs/PRODUCT.md](docs/PRODUCT.md) | Vision, persona, first vertical, principles |
| [docs/FEATURES.md](docs/FEATURES.md) | Complete feature list with IDs and milestones |
| [docs/USER_STORIES.md](docs/USER_STORIES.md) | User stories with acceptance criteria |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture, request lifecycle, tech stack |
| [docs/DATA_MODEL.md](docs/DATA_MODEL.md) | Artifact types, provenance schema, storage layers |
| [docs/AGENTS.md](docs/AGENTS.md) | Agent roles, tools, LangGraph graph design |
| [docs/SOURCES.md](docs/SOURCES.md) | Source connectors, tiers, auth, rate policies, caching |
| [docs/PLUGIN_SPEC.md](docs/PLUGIN_SPEC.md) | How to add a source connector or tool |
| [docs/UI_UX.md](docs/UI_UX.md) | Workbench layout, card types, interaction model, Figma research plan |
| [docs/EVALUATION.md](docs/EVALUATION.md) | Four-layer testing and benchmark strategy |
| [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) | Research bundle export spec |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Milestones M0–M4 |
| [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Ordered task list for building M0/M1 |
| [docs/adr/](docs/adr/) | Architecture decision records |
| [NON_GOALS.md](NON_GOALS.md) | What v1 explicitly does not do |
| [CLAUDE.md](CLAUDE.md) | Instructions for Claude Code |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Adding a source connector is the most valuable contribution — see [docs/PLUGIN_SPEC.md](docs/PLUGIN_SPEC.md).

## License

BSD-3-Clause for the core (see [LICENSE](LICENSE)). Bundled third-party components (e.g. Aladin Lite, GPL-3) keep their own licenses; see [docs/adr/ADR-0012-aladin-licensing.md](docs/adr/ADR-0012-aladin-licensing.md).

## Citation

If AstroAssist helps your research, please cite it — see [CITATION.cff](CITATION.cff).
