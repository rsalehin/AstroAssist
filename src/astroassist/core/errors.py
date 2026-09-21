"""Exception hierarchy for AstroAssist."""

from __future__ import annotations


class AstroAssistError(Exception):
    """Base class for all AstroAssist errors."""


class ConfigurationError(AstroAssistError):
    """Invalid or missing configuration (profile, provider, credential wiring)."""


class CredentialError(AstroAssistError):
    """A required credential is missing or unusable."""


class ProvenanceError(AstroAssistError):
    """An artifact was produced without valid provenance."""


class ToolError(AstroAssistError):
    """A curated tool failed."""


class SourceError(AstroAssistError):
    """A source connector failed."""


class RateLimitError(SourceError):
    """A source rate limit or circuit breaker tripped."""


class QueryError(SourceError):
    """An external query (TAP/HTTP/astroquery) failed."""
