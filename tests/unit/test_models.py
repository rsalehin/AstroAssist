"""ModelProvider protocol, profiles and adapters [F-CORE-005]."""

from __future__ import annotations

import pytest
from langchain_core.language_models import BaseChatModel

from astroassist.core.config import Settings
from astroassist.core.credentials import CredentialManager
from astroassist.core.errors import ConfigurationError
from astroassist.core.models import (
    PROFILES,
    CompositeProvider,
    ModelProvider,
    RoleModel,
    build_provider,
    make_chat_model,
)


def test_every_profile_defines_all_roles() -> None:
    for profile in PROFILES.values():
        for role in ("router", "planner", "synthesis"):
            spec = profile.role(role)  # type: ignore[arg-type]
            assert spec.provider
            assert spec.model


def test_make_anthropic_requires_credential() -> None:
    cm = CredentialManager(use_keyring=False)
    with pytest.raises(ConfigurationError):
        make_chat_model(RoleModel(provider="anthropic", model="claude-sonnet-5"), cm)


def test_make_anthropic_with_credential() -> None:
    cm = CredentialManager(use_keyring=False)
    cm.set_session("anthropic", "sk-ant-dummy")
    model = make_chat_model(RoleModel(provider="anthropic", model="claude-sonnet-5"), cm)
    assert isinstance(model, BaseChatModel)


def test_make_openai_compatible_builds_offline() -> None:
    cm = CredentialManager(use_keyring=False)
    model = make_chat_model(
        RoleModel(provider="openai-compatible", model="local", base_url="http://localhost:1234/v1"),
        cm,
    )
    assert isinstance(model, BaseChatModel)


def test_composite_provider_is_a_model_provider() -> None:
    cm = CredentialManager(use_keyring=False)
    cm.set_session("anthropic", "sk-ant-dummy")
    provider = CompositeProvider(PROFILES["balanced"], cm)
    assert isinstance(provider, ModelProvider)
    assert isinstance(provider.get_chat_model("synthesis"), BaseChatModel)


def test_build_provider_composite_for_real_profile() -> None:
    cm = CredentialManager(use_keyring=False)
    provider = build_provider(Settings(model_profile="balanced"), credentials=cm)
    assert isinstance(provider, CompositeProvider)


def test_settings_rejects_unknown_profile() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Settings(model_profile="nope")  # type: ignore[arg-type]
