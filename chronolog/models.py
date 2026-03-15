"""Data models for ChronoLog."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class TimeEntry:
    """A single time tracking entry.

    Args:
        id: Database row ID, or None for unsaved entries.
        description: What the user is working on.
        project: Project name this entry belongs to.
        tags: List of string tags for categorisation.
        start_time: UTC-aware datetime when the timer started.
        end_time: UTC-aware datetime when the timer stopped, or None if running.
    """

    id: int | None
    description: str
    project: str
    tags: list[str]
    start_time: datetime
    end_time: datetime | None

    @property
    def duration(self) -> timedelta | None:
        """Return the duration of this entry, or None if still running."""
        if self.end_time is None:
            return None
        return self.end_time - self.start_time

    @property
    def duration_minutes(self) -> float | None:
        """Return the duration in minutes, or None if still running."""
        d = self.duration
        if d is None:
            return None
        return d.total_seconds() / 60.0

    def to_row(self) -> dict[str, Any]:
        """Convert to a dict suitable for DB insertion.

        Tags are serialised as a comma-separated string.
        Datetimes are serialised as ISO-8601 strings.

        Returns:
            Dictionary with string keys ready for database storage.
        """
        return {
            "description": self.description,
            "project": self.project,
            "tags": ",".join(self.tags),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> TimeEntry:
        """Construct a TimeEntry from a database row dict.

        Args:
            row: Dictionary with keys matching DB columns.

        Returns:
            A new TimeEntry instance.
        """
        tags_raw = row["tags"]
        tags = tags_raw.split(",") if tags_raw else []

        end_time_raw = row["end_time"]
        end_time = (
            datetime.fromisoformat(end_time_raw) if end_time_raw else None
        )

        return cls(
            id=row["id"],
            description=row["description"],
            project=row["project"],
            tags=tags,
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=end_time,
        )


@dataclass
class Project:
    """A project that time entries can be grouped under.

    Args:
        name: Unique project name.
        created_at: UTC-aware datetime when the project was created.
        archived: Whether the project is archived (default False).
    """

    name: str
    created_at: datetime
    archived: bool = False
