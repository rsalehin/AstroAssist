# ADR-0003: LangGraph + LangChain tools + LangSmith

**Status:** Accepted · **Date:** 2026-09-21 · **Deciders:** Abir (maintainer)

## Context
Need stateful, resumable, inspectable multi-step workflows with human checkpoints and parallel branches.

## Decision
LangGraph state graph with SQLite checkpointer and interrupts; LangChain tool abstraction; LangSmith opt-in tracing and evaluation.

## Alternatives considered
Plain ReAct loop (no plan visibility, poor parallelism); custom orchestrator (reinventing persistence/HITL); CrewAI/AutoGen (weaker durability/HITL story).

## Consequences
Vendor coupling to LangChain ecosystem; mitigated by keeping artifacts and tools framework-agnostic Pydantic/plain functions.
