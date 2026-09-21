# ADR-0008: Agents split by scientific domain/task; sources are tools

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
One agent per archive scales to dozens of agents and duplicates reasoning.

## Decision
Object & Catalog, Observation, Literature, Time-Domain, Spectroscopy, Compute, Visualization agents; Router, Planner, Supervisor, Synthesis roles. Each source is a plugin exposing tools.

## Alternatives considered
Per-source agents; single monolithic agent.

## Consequences
Adding a source never adds an agent; agents' prompts stay stable.
