# Changelog
## Unreleased
- Project specification, architecture, ADRs and implementation plan (2026-09-21).
- Cross-platform dev setup: `make setup` installs core+dev; `make setup-all` for full stack; ruff excludes Markdown; `.gitattributes` keeps hooks LF.
- Package scaffold finalized: `astroassist version` CLI + tests [F-CORE-001/002].
- Core types: astropy JSON codecs (`QuantityValue`/`SkyCoordValue`/`TimeValue`), `Provenance` + id helpers, and all DATA_MODEL artifact kinds with a discriminated union [F-CORE-003/004].
