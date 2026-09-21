"""Chat routes: post a message and stream the response as SSE."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from astroassist.server.context import AppContext
from astroassist.server.routes.deps import get_ctx
from astroassist.server.stream import run_message_stream

router = APIRouter(prefix="/api", tags=["chat"])


class MessageIn(BaseModel):
    text: str


@router.post("/threads/{thread_id}/messages")
def post_message(
    thread_id: str, body: MessageIn, ctx: AppContext = Depends(get_ctx)
) -> EventSourceResponse:
    thread = ctx.store.get_thread(thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="thread not found")
    return EventSourceResponse(run_message_stream(ctx, thread.workspace_id, thread_id, body.text))
