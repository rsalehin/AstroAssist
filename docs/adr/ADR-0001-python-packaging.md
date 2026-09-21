# ADR-0001: Python 3.11–3.13 with uv + pyproject; conda mirror

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
All domain tooling is Python-native; astronomers mostly use conda; contributors expect modern packaging.

## Decision
Python >=3.11,<3.14. uv + pyproject.toml + uv.lock as the primary system; environment.yml maintained for conda/mamba users; pip install supported.

## Alternatives considered
Poetry (slower, less momentum); conda-only (poor for pip/tool installs); Python 3.10 floor (loses typing features).

## Consequences
Test matrix 3.11/3.12/3.13; two dependency manifests must stay in sync (CI check).
