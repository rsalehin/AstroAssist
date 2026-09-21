# Product definition

## One-liner
A locally-run research workbench that lets astronomers ask questions in natural language and get provenance-tracked, reproducible scientific answers assembled from astronomical archives, Astropy calculations and the literature.

## Primary persona (v1)
**The research-active astronomer** who, in a normal working week, combines object metadata, catalog measurements, archival observations, papers and Python calculations — a PhD student, postdoc or staff scientist. They already use SIMBAD, VizieR, ADS and Jupyter; they distrust anything that cannot show its sources.

Explicitly **not** driving v1 architecture: school/outreach users, amateur observers, undergraduate teaching, general science chat, automated paper writing, telescope control.

## First science vertical
**Stellar / time-domain astrophysics.** One stellar question exercises nearly every capability: name resolution, coordinates, Gaia astrometry, VizieR photometry, MAST/TESS light curves, physical calculations, plots, papers and citations. Extragalactic, radio and lensing verticals follow once the vertical slice is proven.

## Day-one end-to-end story
> Investigate **AD Leo**. Resolve the object, retrieve the best current astrometry and basic stellar properties, calculate distance and tangential velocity, find available TESS observations, download and display a light curve, identify significant flaring activity, find recent papers discussing its magnetic activity, and produce a research summary in which every retrieved number, calculated number, plot, query and citation can be inspected and reproduced.

If this story runs end-to-end with full provenance and exports as a research bundle, v1 is real.

## Product principles (ordered)
1. Correctness
2. Provenance
3. Reproducibility
4. Uncertainty made visible
5. Inspectability (queries, code, trace)
6. Speed
7. Aesthetics

A beautiful hallucinated table is a product failure.

## Core promises to the user
- Every number has a unit, an uncertainty (when known), a source and a way to see the query that produced it.
- Sources that disagree are shown side by side, never silently reconciled.
- A failed or substituted source is reported, with what was *not* retrieved.
- Nothing expensive, risky or destructive runs without asking.
- The whole session can be exported as a runnable notebook, data files and a bibliography.

## Distribution and runtime
- `uv tool install astroassist` / `pip install astroassist` → `astroassist serve` → local FastAPI backend → browser workbench. Docker compose optional. Tauri desktop wrapper considered post-v1.
- Public-data workflows require zero configuration. Credentials only when actually required (ADS token, proprietary MAST/ESO).
- Windows, macOS, Linux supported for the core.
- LLM backend pluggable (Anthropic, OpenAI, OpenAI-compatible, Ollama, vLLM). Offline *LLM* and offline *cached-workspace analysis* are goals; archive queries need internet.

## Core domain objects
`User → Workspace → Session → Thread → Artifact`, plus `Credential`, `Job`, `Query`. v1 is single-user local but modelled so multi-user can be added without rewriting.
