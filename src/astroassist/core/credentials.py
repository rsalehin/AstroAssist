"""Credential manager [F-CORE-007].

Lookup order: OS keyring -> environment variable -> in-memory session store. Tokens never
touch disk in plaintext and are never logged or serialized into artifacts. ``__repr__`` is
deliberately opaque so a credential object cannot leak into a traceback or log line.
"""

from __future__ import annotations

import os

# Map a logical source name to its conventional environment variable.
DEFAULT_ENV_MAP: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "ads": "ADS_DEV_KEY",
    "mast": "MAST_API_TOKEN",
    "langsmith": "LANGSMITH_API_KEY",
}


class CredentialManager:
    """Resolve and store secrets for external services."""

    def __init__(
        self,
        service: str = "astroassist",
        use_keyring: bool = True,
        env_map: dict[str, str] | None = None,
    ) -> None:
        self._service = service
        self._use_keyring = use_keyring
        self._env_map = dict(DEFAULT_ENV_MAP)
        if env_map:
            self._env_map.update(env_map)
        self._session: dict[str, str] = {}

    def _keyring_get(self, source: str) -> str | None:
        if not self._use_keyring:
            return None
        try:
            import keyring

            return keyring.get_password(self._service, source)
        except Exception:
            # Missing/locked backend must never crash a public-data workflow.
            return None

    def _keyring_set(self, source: str, token: str) -> bool:
        if not self._use_keyring:
            return False
        try:
            import keyring

            keyring.set_password(self._service, source, token)
            return True
        except Exception:
            return False

    def get(self, source: str) -> str | None:
        """Return the token for ``source`` or ``None`` (keyring > env > session)."""
        token = self._keyring_get(source)
        if token:
            return token
        env_var = self._env_map.get(source)
        if env_var:
            env_val = os.environ.get(env_var)
            if env_val:
                return env_val
        return self._session.get(source)

    def set(self, source: str, token: str, persist: bool = True) -> None:
        """Store a token. ``persist`` writes to the keyring when available; otherwise the
        value is kept for this session only."""
        if persist and self._keyring_set(source, token):
            return
        self._session[source] = token

    def set_session(self, source: str, token: str) -> None:
        """Store a token for this process only (never persisted)."""
        self._session[source] = token

    def delete(self, source: str) -> None:
        self._session.pop(source, None)
        if self._use_keyring:
            try:
                import keyring

                keyring.delete_password(self._service, source)
            except Exception:
                pass

    def has(self, source: str) -> bool:
        return self.get(source) is not None

    def __repr__(self) -> str:
        return f"CredentialManager(service={self._service!r}, sources={sorted(self._session)})"
