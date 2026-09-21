"""Workspace and thread routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from astroassist.server.context import AppContext
from astroassist.server.routes.deps import get_ctx

router = APIRouter(prefix="/api", tags=["workspaces"])


class WorkspaceIn(BaseModel):
    name: str


class ThreadIn(BaseModel):
    title: str | None = None


@router.get("/bootstrap")
def bootstrap(ctx: AppContext = Depends(get_ctx)) -> dict[str, str]:
    workspace_id, thread_id = ctx.ensure_default_thread()
    return {"workspace_id": workspace_id, "thread_id": thread_id}


@router.get("/workspaces")
def list_workspaces(ctx: AppContext = Depends(get_ctx)) -> list[dict[str, str]]:
    return [
        {"id": w.id, "name": w.name, "created_at": w.created_at.isoformat()}
        for w in ctx.store.list_workspaces()
    ]


@router.post("/workspaces")
def create_workspace(body: WorkspaceIn, ctx: AppContext = Depends(get_ctx)) -> dict[str, str]:
    ws = ctx.store.create_workspace(body.name)
    return {"id": ws.id, "name": ws.name}


@router.post("/workspaces/{workspace_id}/threads")
def create_thread(
    workspace_id: str, body: ThreadIn, ctx: AppContext = Depends(get_ctx)
) -> dict[str, str]:
    if ctx.store.get_workspace(workspace_id) is None:
        raise HTTPException(status_code=404, detail="workspace not found")
    thread = ctx.store.create_thread(workspace_id, title=body.title)
    return {"id": thread.id, "workspace_id": workspace_id}


@router.get("/workspaces/{workspace_id}/artifacts")
def list_artifacts(workspace_id: str, ctx: AppContext = Depends(get_ctx)) -> list[dict[str, str]]:
    return [
        {"id": a.id, "kind": a.kind, "summary": a.summary}
        for a in ctx.store.list_artifacts(workspace_id)
    ]
