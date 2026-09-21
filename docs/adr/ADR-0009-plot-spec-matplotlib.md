# ADR-0009: Declarative plot spec → matplotlib; Plotly optional

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Researchers need publication-quality static figures and reproducible edits.

## Decision
Plots are built from a JSON spec via typed plot tools; matplotlib renders SVG/PNG by default; Plotly toggle for interactivity; NL edits mutate the spec and regenerate code.

## Alternatives considered
Always let the LLM write matplotlib (irreproducible edits); Plotly-only (weaker publication output).

## Consequences
Spec layer to maintain; every plot has code+data+spec; edits are versioned.
