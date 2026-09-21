# ADR-0010: Workbench UI with React/TypeScript

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Chat alone loses state; researchers need tables, plots, sky and code side by side.

## Decision
Three-pane workbench (rail / chat / artifact viewer) + trace/jobs bar; React + TS + Vite + Tailwind; Aladin Lite embedded.

## Alternatives considered
Pure chat; Jupyter-only; Streamlit (limits UX).

## Consequences
Frontend is a real app; design in Figma before build.
