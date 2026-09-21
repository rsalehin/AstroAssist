"""Application configuration [F-CORE-008].

Zero-config defaults so public-data workflows need no setup. Precedence, lowest to highest:
built-in defaults < ``~/.astroassist/config.toml`` < environment (``ASTROASSIST_*``) < explicit
init kwargs. The data directory holds workspaces, schemas and logs (see DATA_MODEL.md).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

ModelProfile = Literal["economy", "balanced", "research", "local", "mock"]
CacheMode = Literal["online", "prefer_cache", "offline"]


def default_data_dir() -> Path:
    env = os.environ.get("ASTROASSIST_DATA_DIR")
    return Path(env).expanduser() if env else Path.home() / ".astroassist"


def default_config_path() -> Path:
    return default_data_dir() / "config.toml"


class RiskThresholds(BaseSettings):
    """Preflight thresholds above which a step needs human approval (M1 uses these)."""

    cone_radius_arcsec: float = 300.0
    max_rows: int = 100_000
    max_bytes: int = 50_000_000
    async_seconds: int = 30


class Settings(BaseSettings):
    """Top-level runtime settings."""

    model_config = SettingsConfigDict(
        env_prefix="ASTROASSIST_",
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    model_profile: ModelProfile = "balanced"
    host: str = "127.0.0.1"
    port: int = 8765
    data_dir: Path = Field(default_factory=default_data_dir)
    cache_mode: CacheMode = "online"

    langsmith_tracing: bool = False
    langsmith_project: str = "astroassist-dev"

    thresholds: RiskThresholds = Field(default_factory=RiskThresholds)

    @property
    def workspaces_dir(self) -> Path:
        return self.data_dir / "workspaces"

    @property
    def schemas_dir(self) -> Path:
        return self.data_dir / "schemas"

    @property
    def logs_dir(self) -> Path:
        return self.data_dir / "logs"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Order = precedence, highest first: init > env > dotenv > TOML > secrets.
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


def load_settings(config_path: Path | None = None) -> Settings:
    """Load settings, reading ``config.toml`` (default: ``~/.astroassist/config.toml``)."""
    path = config_path or default_config_path()
    Settings.model_config["toml_file"] = str(path)
    return Settings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached process-wide settings."""
    return load_settings()
