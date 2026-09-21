# User stories

Format: **As a** researcher **I want** … **so that** …, with acceptance criteria (AC). Story IDs map to feature IDs in FEATURES.md.

## Epic A — Object identity and basic data (M1)

**US-A1 Resolve an object.** As a researcher I want to type "AD Leo" and get its canonical name, aliases, coordinates, object type and spectral type so that I don't have to look up identifiers across surveys.
AC: `ResolvedObject` artifact; SIMBAD as resolver with Sesame fallback; aliases include GJ/HIP/Gaia DR3 ids; object cached for the session; object card rendered; resolver query visible.

**US-A2 Enter coordinates any way I like.** As a researcher I want to paste `10:19:36.3 +19:52:12` or `164.12 +19.87` or `l=225.3 b=47.0` so that I can search by position without reformatting.
AC: all forms parsed via SkyCoord; normalized ICRS deg stored; displayed forms only when useful.

**US-A3 Get the distance with provenance.** As a researcher I want "What is the distance to AD Leo?" to return the Gaia DR3 parallax, the derived distance with uncertainty, and the literature value from SIMBAD so that I know where each number came from.
AC: `ScientificValue` for parallax (source Gaia DR3, record id) and distance (method inverse_parallax, inputs lineage, code hash); SIMBAD value shown as context; disagreement banner if inconsistent beyond uncertainty; value cards clickable to show query.

**US-A4 Convert units.** "Give that in light-years." AC: Astropy conversion; original artifact untouched; new derived artifact with lineage.

## Epic B — Catalog queries (M1–M2)

**US-B1 Cone search Gaia.** "Gaia sources within 2 arcmin of AD Leo with parallax > 10 mas." AC: ADQL generated, shown, editable; TAP_SCHEMA-aware; result `CatalogTable` with units; table viewer with sort/filter/export.

**US-B2 Expensive query confirmation.** "All Gaia sources within 5 degrees." AC: preflight estimate; confirmation dialog with narrow/continue; no execution without approval.

**US-B3 Self-correcting ADQL.** AC: on service error, up to two schema-aware corrections; then error surfaced with generated query, service response, suggested fix.

**US-B4 VizieR catalog discovery.** "Which VizieR catalogs have photometry for this position?" AC: catalog list with references; selected catalog cone search; catalog paper added to bibliography.

**US-B5 Crossmatch.** "Crossmatch this table with 2MASS within 1 arcsec." AC: `crossmatch` tool; match table with separation column; unmatched count reported.

## Epic C — Observations and time series (M2)

**US-C1 Find TESS data.** "What TESS observations exist for AD Leo?" AC: `ObservationList` with sectors, cadence, product types; observation cards with download action; large download confirmation.

**US-C2 Load and plot a light curve.** "Download sector 45 and plot the light curve." AC: lightkurve fetch → `LightCurve` artifact (Time, flux Quantity, flux_err) → typed light-curve plot tool → `PlotArtifact` with data + code + spec.

**US-C3 Find flares.** "Flag flares above 5σ." AC: `flare_detect` tool; mask + table of events; highlighted plot; every threshold recorded in provenance.

**US-C4 Periodogram and phase fold.** AC: Lomb–Scargle `FitResult`/periodogram plot; phase-folded plot at best period.

**US-C5 Long-running job.** AC: async Gaia job runs in background; job panel shows status, elapsed, cancel; chat remains usable; result artifact appears when done.

## Epic D — Literature (M2–M3)

**US-D1 Find papers.** "Recent papers on AD Leo magnetic activity since 2020." AC: ADS query visible; `LiteratureSet` with paper cards (title, authors, year, abstract, citations, ADS link); token prompted once and stored in keyring.

**US-D2 Bibliography accumulates.** AC: every source used (ADS bibcode, VizieR catalog reference, Gaia DR3 paper) appears in workspace references; `references.bib` exportable.

**US-D3 Search my local library.** AC: local RAG results visibly labelled LOCAL PAPER, distinct from ADS abstracts; evidence snippets with page refs.

## Epic E — Computation (M1–M2)

**US-E1 Deterministic calculation.** "Tangential velocity from these Gaia values." AC: curated tool; inputs referenced by artifact id; no LLM arithmetic.

**US-E2 Custom code with approval.** "Fit a two-component flare model with my own function." AC: proposed Python shown; Run/Edit/Cancel; runs in persistent kernel; `CodeArtifact` with stdout, outputs and provenance.

**US-E3 Persistent kernel.** AC: variables from earlier turns available; restart/clear/inspect controls; resource limits enforced.

**US-E4 Observation planning.** "When is AD Leo observable from Tautenburg tonight?" AC: astroplan tools; altitude/airmass plot; twilight and moon separation reported.

## Epic F — Visualization (M1–M3)

**US-F1 Edit a plot by talking.** "Make x log, add error bars, label the flares." AC: plot spec modified; code regenerated; previous version retained.

**US-F2 See the sky.** "Show the field around AD Leo." AC: Aladin Lite with DSS/Pan-STARRS layers; Gaia overlay of the last cone search; footprints of MAST observations.

**US-F3 Publication export.** AC: SVG/PDF export; code and data exported alongside.

## Epic G — Trust, failure and transparency (M2)

**US-G1 Source down.** AC: explicit "NED unavailable; fallback SIMBAD used; NED-specific photometry NOT retrieved."

**US-G2 Research trace.** AC: per-step source and duration list; click to open query artifact.

**US-G3 Cost visibility.** AC: optional per-run token cost by role.

## Epic H — Reproducibility (M3)

**US-H1 Export bundle.** AC: `analysis.ipynb`, `analysis.py`, lockfile, queries/, data/, figures/, references.bib, provenance.json, README; bundle runs standalone in a fresh environment.

**US-H2 Re-run a query later.** AC: query artifact rerun with cache bypass; new artifact version linked to old.

## Epic I — Setup (M0–M1)

**US-I1 Zero-config start.** AC: `astroassist serve` works with no credentials for SIMBAD/Gaia/VizieR/MAST public data.
**US-I2 Model choice.** AC: settings choose provider + profile; local Ollama works.
**US-I3 Windows.** AC: core install and day-one story pass on Windows CI.
