"""Core business logic for ChronoLog."""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from chronolog.db import get_connection, init_db
from chronolog.exceptions import (
    EntryNotFoundError,
    InvalidProjectNameError,
    NoActiveTimerError,
    ProjectExistsError,
    ProjectNotFoundError,
    TimerAlreadyRunningError,
)
from chronolog.models import Project, TimeEntry


_PROJECT_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-]*$")


def _validate_project_name(name: str) -> None:
    """Validate a project name.

    Args:
        name: The project name to validate.

    Raises:
        InvalidProjectNameError: If the name is invalid.
    """
    if not name or len(name) > 50 or not _PROJECT_NAME_RE.match(name):
        raise InvalidProjectNameError(
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
        InvalidProjectNameError: If the name is invalid.
        ProjectExistsError: If the project already exists.
    """
    _validate_project_name(name)
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        existing = conn.execute(
            "SELECT name FROM projects WHERE name = ?", (name,)
        ).fetchone()
        if existing:
            raise ProjectExistsError(f"Project '{name}' already exists.")
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
        ProjectNotFoundError: If project doesn't exist, is already archived, or is "general".
    """
    if name == "general":
        raise ProjectNotFoundError("Cannot archive the 'general' project.")
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT name, created_at, archived FROM projects WHERE name = ?",
            (name,),
        ).fetchone()
        if row is None:
            raise ProjectNotFoundError(f"Project '{name}' does not exist.")
        if row["archived"]:
            raise ProjectNotFoundError(f"Project '{name}' is already archived.")
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
        TimerAlreadyRunningError: If a timer is already running.
        ProjectNotFoundError: If the project doesn't exist.
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
            raise TimerAlreadyRunningError("A timer is already running — stop it first")

        # Check project exists
        proj = conn.execute(
            "SELECT name FROM projects WHERE name = ?", (project,)
        ).fetchone()
        if proj is None:
            raise ProjectNotFoundError(
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
        NoActiveTimerError: If no timer is currently running.
    """
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM entries WHERE end_time IS NULL"
        ).fetchone()
        if row is None:
            raise NoActiveTimerError("No timer is currently running")

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





def edit_entry(
    db_path: Path,
    entry_id: int,
    description: str | None = None,
    project: str | None = None,
    tags: list[str] | None = None,
) -> TimeEntry:
    """Edit an existing time entry."""
    conn = get_connection(db_path)
    try:
        row = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
        if row is None:
            raise EntryNotFoundError(f'No entry with id {entry_id}')
        if project is not None:
            proj = conn.execute('SELECT name FROM projects WHERE name = ?', (project,)).fetchone()
            if proj is None:
                raise ProjectNotFoundError(f"No such project: '{project}'")
        updates = {}
        if description is not None:
            updates['description'] = description
        if project is not None:
            updates['project'] = project
        if tags is not None:
            updates['tags'] = ','.join(tags)
        if updates:
            set_clause = ', '.join(f'{k} = ?' for k in updates)
            values = list(updates.values()) + [entry_id]
            conn.execute(f'UPDATE entries SET {set_clause} WHERE id = ?', values)
            conn.commit()
        updated = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
        tags_raw = updated['tags']
        tag_list = tags_raw.split(',') if tags_raw else []
        end_raw = updated['end_time']
        end_time = datetime.fromisoformat(end_raw) if end_raw else None
        return TimeEntry(
            id=updated['id'], description=updated['description'],
            project=updated['project'], tags=tag_list,
            start_time=datetime.fromisoformat(updated['start_time']),
            end_time=end_time,
        )
    finally:
        conn.close()


def delete_entry(db_path: Path, entry_id: int) -> None:
    """Delete a time entry by ID."""
    conn = get_connection(db_path)
    try:
        row = conn.execute('SELECT id FROM entries WHERE id = ?', (entry_id,)).fetchone()
        if row is None:
            raise EntryNotFoundError(f'No entry with id {entry_id}')
        conn.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        conn.commit()
    finally:
        conn.close()



def list_tags(db_path: Path) -> list[dict]:
    """List all tags with total time and entry count."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            'SELECT tags, start_time, end_time FROM entries WHERE end_time IS NOT NULL'
        ).fetchall()
        tag_stats: dict[str, dict] = {}
        for row in rows:
            tags_raw = row['tags']
            if not tags_raw:
                continue
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
            start = datetime.fromisoformat(row['start_time'])
            end = datetime.fromisoformat(row['end_time'])
            minutes = (end - start).total_seconds() / 60.0
            for tag in tags:
                if tag not in tag_stats:
                    tag_stats[tag] = {'tag': tag, 'total_minutes': 0.0, 'entry_count': 0}
                tag_stats[tag]['total_minutes'] += minutes
                tag_stats[tag]['entry_count'] += 1
        return sorted(tag_stats.values(), key=lambda x: x['total_minutes'], reverse=True)
    finally:
        conn.close()


def report_weekly(db_path: Path) -> list[dict]:
    """Return per-project summaries for the current week (Monday-Sunday).

    Args:
        db_path: Path to the SQLite database.

    Returns:
        List of dicts with keys: project, hours, percentage.
        Sorted by hours descending. Empty list if no entries.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        start_of_week = datetime(monday.year, monday.month, monday.day, tzinfo=timezone.utc)
        end_of_week = datetime(sunday.year, sunday.month, sunday.day, 23, 59, 59, tzinfo=timezone.utc)
        rows = conn.execute(
            "SELECT project, start_time, end_time FROM entries "
            "WHERE end_time IS NOT NULL "
            "AND start_time >= ? AND start_time <= ? ",
            (start_of_week.isoformat(), end_of_week.isoformat()),
        ).fetchall()

        project_minutes: dict[str, float] = {}
        for row in rows:
            start = datetime.fromisoformat(row["start_time"])
            end = datetime.fromisoformat(row["end_time"])
            minutes = (end - start).total_seconds() / 60.0
            project_minutes[row["project"]] = project_minutes.get(row["project"], 0.0) + minutes

        total_minutes = sum(project_minutes.values())
        if total_minutes == 0:
            return []

        summaries = []
        for proj, mins in project_minutes.items():
            hours = mins / 60.0
            percentage = (mins / total_minutes) * 100.0
            summaries.append({"project": proj, "hours": hours, "percentage": percentage})
        summaries.sort(key=lambda x: x["hours"], reverse=True)
        return summaries
    finally:
        conn.close()


def report_daily(db_path: Path, target_date: date) -> list[TimeEntry]:
    """Return completed entries for a given date.

    Args:
        db_path: Path to the SQLite database.
        target_date: The date to query entries for.

    Returns:
        List of completed TimeEntry objects for the given date, ordered by start_time.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        start_of_day = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc)
        end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=timezone.utc)
        rows = conn.execute(
            "SELECT id, description, project, tags, start_time, end_time "
            "FROM entries "
            "WHERE end_time IS NOT NULL "
            "AND start_time >= ? AND start_time <= ? "
            "ORDER BY start_time",
            (start_of_day.isoformat(), end_of_day.isoformat()),
        ).fetchall()
        return [TimeEntry.from_row(dict(row)) for row in rows]
    finally:
        conn.close()


def list_entries(db_path: Path, limit: int = 10) -> list[TimeEntry]:
    """Return recent time entries ordered by start_time descending.

    Args:
        db_path: Path to the SQLite database file.
        limit: Maximum number of entries to return (default 10).

    Returns:
        List of TimeEntry objects, most recent first.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(
            "SELECT id, description, project, tags, start_time, end_time "
            "FROM entries ORDER BY start_time DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        return [TimeEntry.from_row(dict(row)) for row in rows]
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
