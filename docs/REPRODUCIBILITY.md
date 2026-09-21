# Reproducibility bundle

`Export reproducible research bundle` produces:
```
<workspace-slug>/
├── analysis.ipynb        # dependency-ordered cells: queries → data loads → calculations → plots
├── analysis.py           # same as script
├── environment.lock      # uv lock / pip freeze + python version
├── queries/              # gaia_q_01.adql, simbad_q_02.json, ads_q_03.json …
├── data/                 # ECSV/Parquet/FITS payloads referenced by cells
├── figures/              # SVG + PNG, one per PlotArtifact version
├── references.bib        # all citation keys used
├── citations.json        # claim → citation mapping
├── provenance.json       # full artifact lineage graph
└── README.md             # how to run, what was asked, model/profile used, dates
```
Rules:
- Cells load data from `data/` by default and include a commented alternative that re-executes the stored query live.
- Every artifact in the lineage of any artifact shown in the answer is included.
- Credentials are never included; a placeholder documents which tokens a live rerun needs.
- Bundle must execute standalone in a fresh environment (checked by `F-REPRO-004` test).
