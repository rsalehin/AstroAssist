# Plugin specification (source connectors and tools)

A connector adds a data source without touching agents. **Do not freeze this interface before three real connectors exist**; expect revisions through M2.

## SourcePlugin
```python
class SourcePlugin(Protocol):
    manifest: Manifest
    def capabilities(self) -> set[Capability]: ...
    def auth(self) -> AuthSpec: ...                  # public | token | login
    def schema_provider(self) -> SchemaProvider | None: ...  # TAP_SCHEMA mirror, static schema, or None
    def tools(self) -> list[BaseTool]: ...           # typed LangChain tools returning artifacts
    def provenance_adapter(self) -> ProvenanceAdapter: ...   # maps raw responses → Provenance fields, citation keys
    def rate_policy(self) -> RatePolicy: ...
    def cost_estimate(self, tool: str, args: dict) -> CostEstimate: ...
    def health(self) -> HealthStatus: ...
```

## Manifest (YAML next to the package)
```yaml
id: gaia
name: ESA Gaia Archive
homepage: https://gea.esac.esa.int/archive/
capabilities: [resolve_id, catalog_search, cone_search, adql, async_query]
protocols: [TAP, ADQL]
auth: { public: anonymous, optional_login: true }
citation:
  bibcodes: ["2016A&A...595A...1G", "2023A&A...674A...1G"]
cache_ttl: { catalog_rows: 180d }
rate_policy: { max_concurrency: 3, rps: 1, burst: 3, retries: 3, honor_retry_after: true }
risk_thresholds: { cone_radius_deg: 0.5, max_rows: 50000 }
platforms: [linux, macos, windows]
extras: []
```

## Contributor checklist for a new connector
1. `astroassist new-connector <id>` (or Claude Code `/new-connector <id>`) scaffolds `src/astroassist/sources/<id>/` with `manifest.yaml`, `plugin.py`, `tools.py`, `normalize.py`, `tests/`, `README.md`.
2. Implement tools returning artifacts; write `QueryArtifact` for each external call.
3. Implement `normalize.py`: raw response → artifact with units (UCD/unit strings → astropy units), quality flags, source record ids.
4. Provide citation mapping.
5. Record fixtures (`pytest-recording`) for unit tests; add `@pytest.mark.live` contract test.
6. Add benchmark questions in `evals/benchmark/<id>.yaml`.
7. Document in `docs/SOURCES.md`.

## Tool plugin
A tool is a `@tool` with a Pydantic input schema (units declared), returns an artifact, and registers metadata: `domain`, `risk_class` (safe | confirm | code), `cost_estimator`, `version`. Tools must be pure functions of their inputs plus declared side effects (artifact writes).
