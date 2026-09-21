"""Server application context: settings, store, provider and compiled graph."""

from __future__ import annotations

from dataclasses import dataclass

from astroassist.core.config import Settings, apply_langsmith_env, get_settings
from astroassist.core.credentials import CredentialManager
from astroassist.core.models.base import ModelProvider, build_provider
from astroassist.workflows.graph import build_graph, make_sqlite_checkpointer
from astroassist.workspace.store import WorkspaceStore


@dataclass
class AppContext:
    settings: Settings
    store: WorkspaceStore
    provider: ModelProvider
    graph: object  # compiled LangGraph

    @classmethod
    def build(cls, settings: Settings | None = None) -> AppContext:
        settings = settings or get_settings()
        apply_langsmith_env(settings)
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        store = WorkspaceStore(settings.data_dir)
        provider = build_provider(settings, CredentialManager())
        checkpointer = make_sqlite_checkpointer(settings.data_dir / "checkpoints.db")
        graph = build_graph(provider, checkpointer=checkpointer)
        return cls(settings=settings, store=store, provider=provider, graph=graph)

    def ensure_default_thread(self) -> tuple[str, str]:
        """Return (workspace_id, thread_id), creating a default workspace/thread if needed."""
        workspaces = self.store.list_workspaces()
        ws = workspaces[0] if workspaces else self.store.create_workspace("Default workspace")
        threads = self.store.list_threads(ws.id)
        thread = threads[0] if threads else self.store.create_thread(ws.id, title="Main thread")
        return ws.id, thread.id
