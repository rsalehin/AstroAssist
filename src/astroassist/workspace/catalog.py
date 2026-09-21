"""DuckDB artifact catalog [F-WS-002].

An analytical index over the artifact files: it enables querying/paging artifacts and (from M1)
column-level metadata and analytics over Parquet payloads without loading them into memory.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb


class ArtifactCatalog:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(self.db_path))
        self._init()

    def _init(self) -> None:
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                id VARCHAR PRIMARY KEY,
                workspace_id VARCHAR,
                thread_id VARCHAR,
                kind VARCHAR,
                summary VARCHAR,
                path VARCHAR,
                created_at TIMESTAMP
            )
            """
        )

    def register(
        self,
        artifact_id: str,
        workspace_id: str,
        kind: str,
        summary: str,
        path: str,
        thread_id: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.con.execute(
            """
            INSERT OR REPLACE INTO artifacts
                (id, workspace_id, thread_id, kind, summary, path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                artifact_id,
                workspace_id,
                thread_id,
                kind,
                summary,
                path,
                created_at or datetime.now(tz=UTC),
            ],
        )

    def _row_to_dict(self, row: tuple[Any, ...]) -> dict[str, Any]:
        cols = ["id", "workspace_id", "thread_id", "kind", "summary", "path", "created_at"]
        return dict(zip(cols, row, strict=True))

    def list(self, workspace_id: str | None = None) -> list[dict[str, Any]]:
        if workspace_id is None:
            cur = self.con.execute("SELECT * FROM artifacts ORDER BY created_at")
        else:
            cur = self.con.execute(
                "SELECT * FROM artifacts WHERE workspace_id = ? ORDER BY created_at",
                [workspace_id],
            )
        return [self._row_to_dict(r) for r in cur.fetchall()]

    def get(self, artifact_id: str) -> dict[str, Any] | None:
        cur = self.con.execute("SELECT * FROM artifacts WHERE id = ?", [artifact_id])
        row = cur.fetchone()
        return self._row_to_dict(row) if row else None

    def close(self) -> None:
        self.con.close()
