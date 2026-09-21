# ADR-0006: DuckDB catalog + SQLite metadata/checkpoints + files

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Need analytics over tables, durable graph state, and native scientific file formats.

## Decision
DuckDB for artifact catalog and analytics over Parquet; SQLite for workspace metadata and LangGraph checkpoints; filesystem for FITS/ECSV/Parquet/images/raw responses.

## Alternatives considered
Postgres (heavy for local); single SQLite for everything (poor analytics); MongoDB (unnecessary).

## Consequences
Three storage concerns, each simple; all embedded, zero-ops.
