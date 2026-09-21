# ADR-0004: Pluggable model providers with role-based profiles

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Users vary between cloud and institute-constrained/offline setups; different roles need different cost/quality.

## Decision
`ModelProvider` protocol; adapters for Anthropic, OpenAI, OpenAI-compatible, Ollama, vLLM; profiles economy/balanced/research/local assign models per role (router/planner/synthesis).

## Alternatives considered
Single hard-coded provider.

## Consequences
Extra abstraction; prompts must be robust across models; local models tested in CI with a small model where feasible.
