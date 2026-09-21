# Open questions

Add here whenever a scientific or design convention is unclear instead of guessing.

- Parallax zero-point correction: apply Lindegren+2021 by default, or report naive with warning? (Current: naive + warning; probabilistic distance optional.)
- Epoch propagation default when comparing Gaia (J2016.0) with older catalogs.
- Magnitude system tagging (Vega/AB) in `CatalogTable` column metadata — use UCD + explicit `mag_system` key.
- Aladin Lite bundling vs CDN loading with respect to GPL-3 and offline mode.
- Local literature library: run as separate service (existing FastAPI) or vendor as optional extra?
