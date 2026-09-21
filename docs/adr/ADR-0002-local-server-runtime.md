# ADR-0002: Local Python server + browser workbench; desktop wrapper later

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
The hard dependency is the scientific Python environment, not a desktop shell.

## Decision
`astroassist serve` runs FastAPI on localhost and opens the browser UI. Docker compose optional. Tauri wrapper deferred to post-v1.

## Alternatives considered
Electron/Tauri first (packaging complexity without solving science); Jupyter extension (constrains UI); hosted SaaS (data policy, cost, contradicts local-first).

## Consequences
Simple install; UI is a normal web app; later Tauri can wrap it unchanged.
