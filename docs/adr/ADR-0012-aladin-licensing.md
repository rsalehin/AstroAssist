# ADR-0012: Embed Aladin Lite while keeping core BSD-3

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Aladin Lite is GPL-3; core is BSD-3-Clause.

## Decision
Load Aladin Lite as a separately licensed component (not compiled into the BSD core bundle); document licensing in NOTICE; evaluate CDN vs vendored loading for offline mode.

## Alternatives considered
Reimplement a sky viewer (huge); skip sky view (major UX loss).

## Consequences
License clarity; offline mode needs explicit handling.
