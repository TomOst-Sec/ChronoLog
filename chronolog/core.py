"""Core business logic for ChronoLog."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from chronolog.db import get_connection
from chronolog.models import TimeEntry


def start_timer(
    db_path: Path,
    description: str,
    project: str = "general",
    tags: list[str] | None = None,
) -> TimeEntry:
    """Start a new timer.

    Args:
        db_path: Path to the SQLite database.
        description: What the user is working on.
        project: Project name (must already exist in DB).
        tags: Optional list of tags.

    Returns:
        The newly created TimeEntry.

    Raises:
        RuntimeError: If a timer is already running or the project doesn't exist.
    """
    if tags is None:
        tags = []

    conn = get_connection(db_path)
    try:
        # Check for already running timer
        row = conn.execute(
            "SELECT id FROM entries WHERE end_time IS NULL"
        ).fetchone()
        if row is not None:
            raise RuntimeError("A timer is already running — stop it first")

        # Check project exists
        proj = conn.execute(
            "SELECT name FROM projects WHERE name = ?", (project,)
        ).fetchone()
        if proj is None:
            raise RuntimeError(
                f"No such project: '{project}' — create it first"
            )

        now = datetime.now(timezone.utc)
        tags_str = ",".join(tags)
        cursor = conn.execute(
            """INSERT INTO entries (description, project, tags, start_time, end_time, created_at)
               VALUES (?, ?, ?, ?, NULL, ?)""",
            (description, project, tags_str, now.isoformat(), now.isoformat()),
        )
        conn.commit()

        return TimeEntry(
            id=cursor.lastrowid,
            description=description,
            project=project,
            tags=tags,
            start_time=now,
            end_time=None,
        )
    finally:
        conn.close()


def stop_timer(db_path: Path) -> TimeEntry:
    """Stop the currently running timer.

    Args:
        db_path: Path to the SQLite database.

    Returns:
        The completed TimeEntry with end_time set.

    Raises:
        RuntimeError: If no timer is currently running.
    """
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM entries WHERE end_time IS NULL"
        ).fetchone()
        if row is None:
            raise RuntimeError("No timer is currently running")

        now = datetime.now(timezone.utc)
        conn.execute(
            "UPDATE entries SET end_time = ? WHERE id = ?",
            (now.isoformat(), row["id"]),
        )
        conn.commit()

        tags_raw = row["tags"]
        tags = tags_raw.split(",") if tags_raw else []

        return TimeEntry(
            id=row["id"],
            description=row["description"],
            project=row["project"],
            tags=tags,
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=now,
        )
    finally:
        conn.close()


def get_active_timer(db_path: Path) -> TimeEntry | None:
    """Get the currently running timer, if any.

    Args:
        db_path: Path to the SQLite database.

    Returns:
        The active TimeEntry, or None if no timer is running.
    """
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM entries WHERE end_time IS NULL"
        ).fetchone()
        if row is None:
            return None

        tags_raw = row["tags"]
        tags = tags_raw.split(",") if tags_raw else []

        return TimeEntry(
            id=row["id"],
            description=row["description"],
            project=row["project"],
            tags=tags,
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=None,
        )
    finally:
        conn.close()
