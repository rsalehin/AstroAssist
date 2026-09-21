"""Structured logging with secret redaction [F-CORE-009].

Tokens must never reach logs or LangSmith. The :func:`redact_processor` runs in every log
pipeline: it blanks values under sensitive keys and masks token-shaped substrings inside
free-text values (e.g. ``Authorization: Bearer ...``).
"""

from __future__ import annotations

import logging
import re
from typing import Any

import structlog
from structlog.typing import EventDict, WrappedLogger

REDACTED = "***REDACTED***"

SENSITIVE_KEY_PARTS = (
    "token",
    "api_key",
    "apikey",
    "secret",
    "password",
    "passwd",
    "authorization",
    "credential",
    "access_key",
)

_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(Bearer\s+)\S+", re.IGNORECASE),
    re.compile(r"\b(?:sk-|gho_|ghp_|ghs_|xox[baprs]-)[A-Za-z0-9_\-]{6,}"),
    re.compile(r"((?:api[_-]?key|token|password|secret)\s*[=:]\s*)\S+", re.IGNORECASE),
)


def _mask_str(text: str) -> str:
    text = _PATTERNS[0].sub(rf"\1{REDACTED}", text)
    text = _PATTERNS[1].sub(REDACTED, text)
    text = _PATTERNS[2].sub(rf"\1{REDACTED}", text)
    return text


def redact_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    """structlog processor that removes secrets from a log event."""
    for key, value in list(event_dict.items()):
        if any(part in key.lower() for part in SENSITIVE_KEY_PARTS):
            event_dict[key] = REDACTED
        elif isinstance(value, str):
            event_dict[key] = _mask_str(value)
    return event_dict


def configure_logging(level: str = "INFO", json_logs: bool = False) -> None:
    """Configure structlog once at process start."""
    renderer: Any = (
        structlog.processors.JSONRenderer() if json_logs else structlog.dev.ConsoleRenderer()
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            redact_processor,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelNamesMapping().get(level.upper(), logging.INFO)
        ),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
