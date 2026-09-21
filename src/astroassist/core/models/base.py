"""Model provider protocol, profiles and adapters [F-CORE-005]."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, SecretStr

from astroassist.core.credentials import CredentialManager
from astroassist.core.errors import ConfigurationError

if TYPE_CHECKING:
    from astroassist.core.config import Settings

ModelRole = Literal["router", "planner", "synthesis"]
ROLES: tuple[ModelRole, ...] = ("router", "planner", "synthesis")

# Provider identifiers accepted by ``make_chat_model``.
Provider = Literal["anthropic", "openai", "openai-compatible", "ollama", "vllm"]


class RoleModel(BaseModel):
    provider: Provider
    model: str
    temperature: float = 0.0
    base_url: str | None = None


class ProfileConfig(BaseModel):
    router: RoleModel
    planner: RoleModel
    synthesis: RoleModel

    def role(self, role: ModelRole) -> RoleModel:
        return {"router": self.router, "planner": self.planner, "synthesis": self.synthesis}[role]


# Sensible defaults; every value is overridable via config. Names use current model ids.
_ANTHROPIC_SMALL = "claude-haiku-4-5-20251001"
_ANTHROPIC_STRONG = "claude-sonnet-5"
_ANTHROPIC_RESEARCH = "claude-opus-5"

PROFILES: dict[str, ProfileConfig] = {
    "economy": ProfileConfig(
        router=RoleModel(provider="anthropic", model=_ANTHROPIC_SMALL),
        planner=RoleModel(provider="anthropic", model=_ANTHROPIC_STRONG),
        synthesis=RoleModel(provider="anthropic", model=_ANTHROPIC_STRONG),
    ),
    "balanced": ProfileConfig(
        router=RoleModel(provider="anthropic", model=_ANTHROPIC_SMALL),
        planner=RoleModel(provider="anthropic", model=_ANTHROPIC_STRONG),
        synthesis=RoleModel(provider="anthropic", model=_ANTHROPIC_STRONG),
    ),
    "research": ProfileConfig(
        router=RoleModel(provider="anthropic", model=_ANTHROPIC_STRONG),
        planner=RoleModel(provider="anthropic", model=_ANTHROPIC_RESEARCH),
        synthesis=RoleModel(provider="anthropic", model=_ANTHROPIC_RESEARCH),
    ),
    "local": ProfileConfig(
        router=RoleModel(provider="ollama", model="llama3.1:8b"),
        planner=RoleModel(provider="ollama", model="llama3.1:70b"),
        synthesis=RoleModel(provider="ollama", model="llama3.1:70b"),
    ),
}

# Which credential source each provider draws its key from.
_PROVIDER_CREDENTIAL: dict[str, str | None] = {
    "anthropic": "anthropic",
    "openai": "openai",
    "openai-compatible": "openai",
    "vllm": None,
    "ollama": None,
}


@runtime_checkable
class ModelProvider(Protocol):
    name: str

    def get_chat_model(self, role: ModelRole) -> BaseChatModel: ...


def make_chat_model(spec: RoleModel, credentials: CredentialManager) -> BaseChatModel:
    """Construct a LangChain chat model for a role spec. Imports are lazy so a mock-only run
    never needs a provider SDK configured."""
    cred_source = _PROVIDER_CREDENTIAL.get(spec.provider)
    api_key = credentials.get(cred_source) if cred_source else None

    if spec.provider == "anthropic":
        if not api_key:
            raise ConfigurationError(
                "No Anthropic credential; set ANTHROPIC_API_KEY or use keyring."
            )
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model_name=spec.model,
            temperature=spec.temperature,
            api_key=SecretStr(api_key),
            timeout=None,
            stop=None,
        )

    if spec.provider in ("openai", "openai-compatible", "vllm"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=spec.model,
            temperature=spec.temperature,
            api_key=SecretStr(api_key or "not-needed"),
            base_url=spec.base_url,
        )

    if spec.provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=spec.model, temperature=spec.temperature, base_url=spec.base_url)

    raise ConfigurationError(f"Unknown model provider: {spec.provider}")


class CompositeProvider:
    """A provider that resolves each role to its configured chat model."""

    def __init__(self, profile: ProfileConfig, credentials: CredentialManager) -> None:
        self.name = "composite"
        self._profile = profile
        self._credentials = credentials

    def role_spec(self, role: ModelRole) -> RoleModel:
        return self._profile.role(role)

    def get_chat_model(self, role: ModelRole) -> BaseChatModel:
        return make_chat_model(self._profile.role(role), self._credentials)


def build_provider(
    settings: Settings, credentials: CredentialManager | None = None
) -> ModelProvider:
    """Build the provider for the active profile. ``mock`` returns the scripted provider."""
    creds = credentials or CredentialManager()
    if settings.model_profile == "mock":
        from astroassist.core.models.mock import MockModelProvider

        return MockModelProvider.default()
    profile = PROFILES.get(settings.model_profile)
    if profile is None:
        raise ConfigurationError(f"Unknown model profile: {settings.model_profile}")
    return CompositeProvider(profile, creds)
