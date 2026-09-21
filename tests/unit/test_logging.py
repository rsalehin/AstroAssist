"""Secret redaction in structured logs [F-CORE-009]."""

from __future__ import annotations

from astroassist.core.logging import REDACTED, redact_processor


def test_redacts_sensitive_keys() -> None:
    event = {"event": "auth", "api_key": "sk-12345", "token": "gho_abcdef", "user": "abir"}
    out = redact_processor(None, "info", dict(event))
    assert out["api_key"] == REDACTED
    assert out["token"] == REDACTED
    assert out["user"] == "abir"


def test_redacts_bearer_in_message() -> None:
    event = {"event": "GET /x", "headers": "Authorization: Bearer sk-secret-xyz"}
    out = redact_processor(None, "info", dict(event))
    assert "sk-secret-xyz" not in str(out["headers"])


def test_non_sensitive_untouched() -> None:
    event = {"event": "resolve", "object": "AD Leo", "duration_ms": 243}
    out = redact_processor(None, "info", dict(event))
    assert out["object"] == "AD Leo"
    assert out["duration_ms"] == 243
