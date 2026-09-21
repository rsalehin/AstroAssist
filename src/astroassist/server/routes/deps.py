"""Shared FastAPI dependency to reach the application context."""

from __future__ import annotations

from fastapi import Request

from astroassist.server.context import AppContext


def get_ctx(request: Request) -> AppContext:
    ctx: AppContext = request.app.state.ctx
    return ctx
