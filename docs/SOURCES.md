# Source connectors

## Tiers
| Tier | Sources | Milestone |
|---|---|---|
| MVP | SIMBAD (+Sesame), Gaia, VizieR, MAST (+lightkurve), ADS | M1–M2 |
| Local | Local literature library (existing hybrid RAG) | M3 |
| Generic | pyvo TAP/SIA/SSA/Cone for any IVOA service | M3 |
| Tier 2 | NED, IRSA (2MASS/WISE/ZTF), HEASARC, ESO, ALMA/NRAO, SDSS, NOIRLab, Pan-STARRS, CADC | M4 |
| Tier 3 | NIST ASD, VALD, CHIANTI, AtomDB, Splatalogue, CDMS/JPL, LAMDA | M4 |
| Tier 4 | AAVSO, TNS, NASA Exoplanet Archive, GWOSC, JPL Horizons, LAMBDA | M4 |

## Auth requirements
| Source | Public access | Credential |
|---|---|---|
| SIMBAD, VizieR, Sesame | anonymous | none |
| Gaia | anonymous (async jobs also anonymous; login for larger quotas) | optional |
| MAST | anonymous for public data | token for proprietary |
| ADS | — | **token required** |
| ESO | anonymous search/download of public data | login for proprietary |
| IRSA, HEASARC, NED | anonymous | none |
Credentials via `CredentialManager` (keyring). The UI prompts only when a capability actually needs a credential.

## Rate policies (initial defaults; tune from experience)
| Source | concurrency | rps | notes |
|---|---|---|---|
| SIMBAD | 2 | 2 | cache aggressively; bulk via script mode |
| VizieR | 2 | 2 | cap MAXREC; TAP for large |
| Gaia | 3 | 1 | async for > 2000 rows or radius > 0.5° |
| MAST | 3 | 2 | downloads in job manager |
| ADS | 1 | 1 | daily quota; cache results 24 h |
Global: exponential backoff + jitter, honor `Retry-After`, circuit breaker after 5 consecutive failures for 5 minutes, request dedup within a run.

## Cache TTL defaults
| Source / data | TTL |
|---|---|
| Gaia DR release catalog rows | 180 d |
| VizieR static catalog rows | 180 d |
| SIMBAD object metadata | 14 d |
| ADS search | 24 h |
| MAST observation metadata | 24 h |
| Downloaded products | permanent (content-addressed) |
| TNS / ZTF alerts | 10 min |
Cache key = source + service_version + normalized query + params + auth scope.

## Risk thresholds (configurable)
- cone radius > 0.5° → confirm
- MAXREC or est_rows > 50 000 → confirm
- est download > 500 MB → confirm
- async job est > 2 min → confirm and run as background job
- proprietary data → confirm
- generated Python → always confirm

## Schema registry
For TAP services mirror `TAP_SCHEMA.schemas/tables/columns` locally at install/refresh; store timestamps; optionally embed column descriptions for planner lookup ("which Gaia table has radial velocity?"). Refresh command: `astroassist schemas refresh gaia`.

## Per-source notes
- **SIMBAD**: astroquery.simbad; request fields: main_id, ids, ra/dec, otype, sp_type, plx, pm, rv, flux(V/G/J/H/K); bibliography via `query_bibobj`. Provide catalog reference key for citation.
- **Gaia**: astroquery.gaia (TAP+); `gaiadr3.gaia_source` default; record `astrometric_params_solved`, `ruwe`, `parallax_over_error` as quality flags; note zero-point caveat in warnings.
- **VizieR**: astroquery.vizier; `find_catalogs` for discovery; catalog reference → bibcode for bibliography; column UCDs preserved.
- **MAST**: astroquery.mast.Observations; `query_criteria`, `get_product_list`, `download_products`; lightkurve `search_lightcurve` for TESS/Kepler; record product provenance (pipeline, version).
- **ADS**: `ads` package or direct API; fields: bibcode,title,author,year,pub,abstract,citation_count,doi,identifier; export BibTeX; respect daily limits.
- **Local library**: adapter over existing FastAPI hybrid RAG (BGE-M3 + BM25 + SPECTER2 + RRF, ADS citation graph); results tagged `origin=local`.
