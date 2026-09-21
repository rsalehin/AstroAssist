# ADR-0005: Astropy Quantity/SkyCoord/Time/QTable as the only scientific representation

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Unit errors are the classic scientific-software failure; LLMs must never do arithmetic on units.

## Decision
All physical numbers are Quantity; positions SkyCoord; times Time; tables QTable. Custom JSON codecs. Conversions only via Astropy.

## Alternatives considered
Plain floats with unit strings (error-prone); pint (not astronomy-aware).

## Consequences
Serialization work; strong correctness guarantees; enables deterministic evaluation.
