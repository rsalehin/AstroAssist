"""FastAPI application [F-CORE-001].

Wires the workspace store, model provider and research graph, mounts the API routers and (when
built) serves the static React workbench from ``frontend/dist``.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from astroassist.core.config import Settings
from astroassist.server.context import AppContext
from astroassist.server.routes import artifacts, chat, interrupts, settings, workspaces


def _frontend_dist() -> Path | None:
    # src/astroassist/server/app.py -> repo root is parents[3]
    candidate = Path(__file__).resolve().parents[3] / "frontend" / "dist"
    return candidate if candidate.is_dir() else None


def create_app(settings_obj: Settings | None = None) -> FastAPI:
    ctx = AppContext.build(settings_obj)
    app = FastAPI(title="AstroAssist", version="0.0.1")
    app.state.ctx = ctx

    # Local dev: allow the Vite dev server origin.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "profile": ctx.settings.model_profile}

    app.include_router(workspaces.router)
    app.include_router(chat.router)
    app.include_router(artifacts.router)
    app.include_router(interrupts.router)
    app.include_router(settings.router)

    dist = _frontend_dist()
    if dist is not None:
        app.mount("/", StaticFiles(directory=str(dist), html=True), name="frontend")

    return app
