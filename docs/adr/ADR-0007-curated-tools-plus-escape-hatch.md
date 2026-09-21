# ADR-0007: Curated deterministic tools first; approved Python escape hatch second

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Arbitrary generated code is capable but non-deterministic and unsafe; curated tools alone are too rigid.

## Decision
Tier 1: typed deterministic tools, no confirmation. Tier 2: LLM proposes Python → user Run/Edit/Cancel → executes in persistent per-workspace kernel with limits → CodeArtifact.

## Alternatives considered
Code-only agent; tools-only agent.

## Consequences
Higher tool-authoring cost; strong provenance and evaluation; user retains control.
