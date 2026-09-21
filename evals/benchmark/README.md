# Benchmark question sets
YAML files, one per source or domain. Schema per item:
```yaml
- id: m1-001
  question: "What is the parallax of Vega?"
  expect:
    sources: [SIMBAD, Gaia DR3]
    tools: [resolve_object, gaia_query_object]
    answer: { value: 130.23, unit: mas, tol: 0.5 }
    provenance: { source: "Gaia DR3", query_id: required }
```
