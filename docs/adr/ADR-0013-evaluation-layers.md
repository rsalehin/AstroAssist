# ADR-0013: Four-layer evaluation with deterministic evaluators first

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Live public services cannot be hit on every commit; LLM judges are weak on scientific correctness.

## Decision
Recorded-fixture unit tests → nightly live contract tests → astronomy benchmark with deterministic unit/tolerance/provenance checks → LangSmith agent-quality metrics.

## Alternatives considered
Live tests in CI; LLM-judge-only evaluation.

## Consequences
Fixture maintenance; strong regression protection.
