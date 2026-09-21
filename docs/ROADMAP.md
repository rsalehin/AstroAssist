# Roadmap

Solo, part-time development. Milestones are vertical slices; each ends with the day-one story further along and all tests green.

## M0 — skeleton (1–2 weeks)
FastAPI app · React shell · LangGraph graph with SQLite checkpointer · workspace/artifact store · ModelProvider abstraction · tool registry · credential manager · CI on 3 OS · repo hygiene. Exit: `astroassist serve` opens an empty workbench; a stub "echo" tool round-trips a typed artifact end-to-end with streaming.

## M1 — vertical slice (3–5 weeks)
SIMBAD + Sesame resolver · Gaia single/cone/ADQL with schema registry · Compute tools (units, coords, distance, velocity) · plot spec + light-curve/scatter plot tools · provenance everywhere · object/value/table/query/plot cards · HITL for large queries and code · escape hatch with persistent kernel · fixtures + contract tests. Exit: "What is the distance and tangential velocity of AD Leo?" fully provenance-tracked with an editable ADQL card.

## M2 — MVP sources (2–4 weeks)
VizieR · MAST + lightkurve · ADS with keyring token · Observation/Literature/Time-Domain agents · flare detection, periodogram, phase fold · Aladin panel · jobs panel · research trace · bibliography · disagreement and fallback notices · slash commands. Exit: day-one AD Leo story runs end-to-end.

## M3 — reproducibility, evaluation, alpha (2–3 weeks)
Research bundle export + standalone re-execution test · query inspector polish · artifact browser · benchmark (≥ 100 questions) + LangSmith evals · local literature adapter · generic pyvo connector · docs site · Docker compose · v0.1.0-alpha on PyPI.

## M4+ — breadth
Tier 2–4 sources (NED, IRSA, HEASARC, ESO, ALMA/NRAO, SDSS, ZTF/AAVSO/TNS, Exoplanet Archive, atomic/molecular DBs, Horizons, GWOSC) · Spectroscopy agent · photometry/imaging tools · MCMC · RM synthesis for ICM work · Tauri wrapper · read-only mobile · notebook sync · JOSS submission.
