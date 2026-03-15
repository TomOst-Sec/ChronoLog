"""Core business logic for ChronoLog."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from chronolog.db import get_connection, init_db
from chronolog.models import Project, TimeEntry


_PROJECT_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-]*$")


def _validate_project_name(name: str) -> None:
    """Validate a project name.

    Args:
        name: The project name to validate.

    Raises:
        ValueError: If the name is invalid.
    """
    if not name or len(name) > 50 or not _PROJECT_NAME_RE.match(name):
        raise ValueError(
            f"Project name '{name}' is invalid. "
            "Names must be 1-50 chars, alphanumeric plus hyphens, "
            "and cannot start with a hyphen."
        )


def create_project(db_path: Path | str, name: str) -> Project:
    """Create a new project.

    Args:
        db_path: Path to the database file.
        name: The project name.

    Returns:
        The created Project.

    Raises:
        ValueError: If the name is invalid or already exists.
    """
    _validate_project_name(name)
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        existing = conn.execute(
            "SELECT name FROM projects WHERE name = ?", (name,)
        ).fetchone()
        if existing:
            raise ValueError(f"Project '{name}' already exists.")
        now = datetime.now(timezone.utc)
        conn.execute(
            "INSERT INTO projects (name, created_at, archived) VALUES (?, ?, 0)",
            (name, now.isoformat()),
        )
        conn.commit()
        return Project(name=name, created_at=now, archived=False)
    finally:
        conn.close()


def list_projects(
    db_path: Path | str, include_archived: bool = False
) -> list[Project]:
    """List all projects.

    Args:
        db_path: Path to the database file.
        include_archived: If True, include archived projects.

    Returns:
        A list of Project instances.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        if include_archived:
            rows = conn.execute(
                "SELECT name, created_at, archived FROM projects ORDER BY name"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT name, created_at, archived FROM projects "
                "WHERE archived = 0 ORDER BY name"
            ).fetchall()
        return [Project.from_row(row) for row in rows]
    finally:
        conn.close()


def archive_project(db_path: Path | str, name: str) -> None:
    """Archive a project.

    Args:
        db_path: Path to the database file.
        name: The project name to archive.

    Raises:
        ValueError: If project doesn't exist, is already archived, or is "general".
    """
    if name == "general":
        raise ValueError("Cannot archive the 'general' project.")
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT name, created_at, archived FROM projects WHERE name = ?",
            (name,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Project '{name}' does not exist.")
        if row["archived"]:
            raise ValueError(f"Project '{name}' is already archived.")
        conn.execute(
            "UPDATE projects SET archived = 1 WHERE name = ?", (name,)
        )
        conn.commit()
    finally:
        conn.close()


def get_project(db_path: Path | str, name: str) -> Project | None:
    """Get a single project by name.

    Args:
        db_path: Path to the database file.
        name: The project name.

    Returns:
        A Project instance, or None if not found.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT name, created_at, archived FROM projects WHERE name = ?",
            (name,),
        ).fetchone()
        if row is None:
            return None
        return Project.from_row(row)
    finally:
        conn.close()


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
