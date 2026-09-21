"""Workspace metadata store and artifact file layout [F-WS-001][F-WS-002].

SQLite (via SQLModel) holds workspace/session/thread/message/artifact-index/job rows. Artifact
payloads are written as JSON under ``workspaces/<ws>/artifacts/<art>/artifact.json`` and larger
binary payloads (Parquet/FITS/SVG) live beside them; only ids and summaries are kept in the row.

M0 uses a single metadata DB (``<data_dir>/workspace.db``) for the local single-user install;
every row is namespaced by ``workspace_id`` so per-workspace databases can be split out for the
multi-user case without a model change. See docs/PROGRESS.md "Needs Abir".
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select

from astroassist.core.artifacts import Artifact, artifact_from_dict, artifact_to_dict
from astroassist.core.provenance import new_id


def _utcnow() -> datetime:
    return datetime.now(tz=UTC)


class Workspace(SQLModel, table=True):
    id: str = Field(default_factory=lambda: new_id("ws"), primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=_utcnow)


class WorkspaceSession(SQLModel, table=True):
    id: str = Field(default_factory=lambda: new_id("ses"), primary_key=True)
    workspace_id: str = Field(index=True, foreign_key="workspace.id")
    title: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)


class Thread(SQLModel, table=True):
    id: str = Field(default_factory=lambda: new_id("thr"), primary_key=True)
    workspace_id: str = Field(index=True, foreign_key="workspace.id")
    session_id: str | None = Field(default=None, foreign_key="workspacesession.id")
    title: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)


class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: new_id("msg"), primary_key=True)
    thread_id: str = Field(index=True, foreign_key="thread.id")
    role: str
    content: str
    seq: int = 0
    created_at: datetime = Field(default_factory=_utcnow)


class ArtifactIndex(SQLModel, table=True):
    id: str = Field(primary_key=True)  # the artifact id (art_...)
    workspace_id: str = Field(index=True, foreign_key="workspace.id")
    thread_id: str | None = Field(default=None, index=True)
    kind: str
    summary: str
    path: str
    created_at: datetime = Field(default_factory=_utcnow)


class JobRecord(SQLModel, table=True):
    id: str = Field(default_factory=lambda: new_id("job"), primary_key=True)
    workspace_id: str = Field(index=True, foreign_key="workspace.id")
    kind: str
    status: str = "queued"
    progress: float = 0.0
    created_at: datetime = Field(default_factory=_utcnow)


class WorkspaceStore:
    """Transactional metadata + artifact persistence for one local install."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = Path(data_dir)
        self.workspaces_root = self.data_dir / "workspaces"
        self.workspaces_root.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "workspace.db"
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        SQLModel.metadata.create_all(self.engine)

    # --- workspaces ---
    def create_workspace(self, name: str) -> Workspace:
        ws = Workspace(name=name)
        with Session(self.engine) as db:
            db.add(ws)
            db.commit()
            db.refresh(ws)
        (self.workspaces_root / ws.id / "artifacts").mkdir(parents=True, exist_ok=True)
        for sub in ("raw", "figures", "data", "exports"):
            (self.workspaces_root / ws.id / sub).mkdir(parents=True, exist_ok=True)
        return ws

    def list_workspaces(self) -> list[Workspace]:
        with Session(self.engine) as db:
            return list(db.exec(select(Workspace).order_by(Workspace.created_at)))

    def get_workspace(self, workspace_id: str) -> Workspace | None:
        with Session(self.engine) as db:
            return db.get(Workspace, workspace_id)

    # --- threads / messages ---
    def create_thread(
        self, workspace_id: str, title: str | None = None, session_id: str | None = None
    ) -> Thread:
        thread = Thread(workspace_id=workspace_id, title=title, session_id=session_id)
        with Session(self.engine) as db:
            db.add(thread)
            db.commit()
            db.refresh(thread)
        return thread

    def get_thread(self, thread_id: str) -> Thread | None:
        with Session(self.engine) as db:
            return db.get(Thread, thread_id)

    def add_message(self, thread_id: str, role: str, content: str) -> Message:
        with Session(self.engine) as db:
            count = len(list(db.exec(select(Message).where(Message.thread_id == thread_id))))
            msg = Message(thread_id=thread_id, role=role, content=content, seq=count)
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return msg

    def list_messages(self, thread_id: str) -> list[Message]:
        with Session(self.engine) as db:
            stmt = select(Message).where(Message.thread_id == thread_id).order_by(Message.seq)
            return list(db.exec(stmt))

    # --- artifacts ---
    def workspace_dir(self, workspace_id: str) -> Path:
        return self.workspaces_root / workspace_id

    def artifact_dir(self, workspace_id: str, artifact_id: str) -> Path:
        return self.workspace_dir(workspace_id) / "artifacts" / artifact_id

    def add_artifact(
        self, workspace_id: str, thread_id: str | None, artifact: Artifact
    ) -> ArtifactIndex:
        adir = self.artifact_dir(workspace_id, artifact.id)
        adir.mkdir(parents=True, exist_ok=True)
        payload_path = adir / "artifact.json"
        payload_path.write_text(json.dumps(artifact_to_dict(artifact), indent=2), encoding="utf-8")
        rel = payload_path.relative_to(self.data_dir).as_posix()
        index = ArtifactIndex(
            id=artifact.id,
            workspace_id=workspace_id,
            thread_id=thread_id,
            kind=artifact.kind,
            summary=artifact.summary,
            path=rel,
        )
        with Session(self.engine) as db:
            db.merge(index)
            db.commit()
        return index

    def get_artifact(self, artifact_id: str) -> Artifact | None:
        with Session(self.engine) as db:
            index = db.get(ArtifactIndex, artifact_id)
        if index is None:
            return None
        payload_path = self.data_dir / index.path
        if not payload_path.exists():
            return None
        return artifact_from_dict(json.loads(payload_path.read_text(encoding="utf-8")))

    def list_artifacts(self, workspace_id: str) -> list[ArtifactIndex]:
        with Session(self.engine) as db:
            stmt = (
                select(ArtifactIndex)
                .where(ArtifactIndex.workspace_id == workspace_id)
                .order_by(ArtifactIndex.created_at)
            )
            return list(db.exec(stmt))

    # --- jobs ---
    def create_job(self, workspace_id: str, kind: str) -> JobRecord:
        job = JobRecord(workspace_id=workspace_id, kind=kind)
        with Session(self.engine) as db:
            db.add(job)
            db.commit()
            db.refresh(job)
        return job

    def list_jobs(self, workspace_id: str) -> Sequence[JobRecord]:
        with Session(self.engine) as db:
            return list(db.exec(select(JobRecord).where(JobRecord.workspace_id == workspace_id)))
