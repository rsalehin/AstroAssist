# ADR-0011: Credentials stored in the OS keyring only

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Tokens must never leak into config, workspace DB, chat history, traces or git.

## Decision
CredentialManager resolves keyring → environment variable → session-only; redaction in logging and LangSmith.

## Alternatives considered
Config file storage.

## Consequences
Requires keyring backend on each OS; headless fallback via env vars.
