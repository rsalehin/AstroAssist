"""Pluggable model providers [F-CORE-005].

A ``ModelProvider`` yields a LangChain chat model per reasoning role (router / planner /
synthesis). Profiles (economy / balanced / research / local) map each role to a concrete
(provider, model). The ``mock`` provider replays scripted responses for deterministic,
key-free tests and e2e runs.
"""

from __future__ import annotations

from astroassist.core.models.base import (
    PROFILES,
    CompositeProvider,
    ModelProvider,
    ModelRole,
    ProfileConfig,
    RoleModel,
    build_provider,
    make_chat_model,
)

__all__ = [
    "PROFILES",
    "CompositeProvider",
    "ModelProvider",
    "ModelRole",
    "ProfileConfig",
    "RoleModel",
    "build_provider",
    "make_chat_model",
]
