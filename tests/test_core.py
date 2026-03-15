"""Tests for ChronoLog core business logic."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from chronolog.core import (
    archive_project,
    create_project,
    delete_entry,
    edit_entry,
    get_active_timer,
    get_project,
    list_projects,
    report_daily,
    report_weekly,
    report_range,
    report_range_summary,
    start_timer,
    stop_timer,
)
from chronolog.db import get_connection, init_db
from chronolog.exceptions import (
    EntryNotFoundError,
    InvalidProjectNameError,
    NoActiveTimerError,
    ProjectExistsError,
    ProjectNotFoundError,
    TimerAlreadyRunningError,
)


@pytest.fixture
def db(tmp_db_path: Path) -> Path:
    """Return an initialised temporary database path."""
    init_db(tmp_db_path)
    return tmp_db_path


class TestStartTimer:
    """Tests for start_timer()."""

    def test_start_timer_basic(self, db: Path) -> None:
        entry = start_timer(db, description="writing code")
        assert entry.description == "writing code"
        assert entry.project == "general"
        assert entry.tags == []
        assert entry.end_time is None
        assert entry.id is not None
        assert entry.start_time.tzinfo is not None

    def test_start_timer_with_project_and_tags(self, db: Path) -> None:
        entry = start_timer(
            db,
            description="feature work",
            project="general",
            tags=["dev", "feature"],
        )
        assert entry.project == "general"
        assert entry.tags == ["dev", "feature"]

    def test_start_timer_raises_if_already_running(self, db: Path) -> None:
        start_timer(db, description="first")
        with pytest.raises(TimerAlreadyRunningError):
            start_timer(db, description="second")

    def test_start_timer_raises_if_project_missing(self, db: Path) -> None:
        with pytest.raises(ProjectNotFoundError):
            start_timer(db, description="task", project="nonexistent")


class TestStopTimer:
    """Tests for stop_timer()."""

    def test_stop_timer(self, db: Path) -> None:
        start_timer(db, description="to stop")
        stopped = stop_timer(db)
        assert stopped.description == "to stop"
        assert stopped.end_time is not None
        assert stopped.end_time >= stopped.start_time

    def test_stop_timer_raises_if_none_running(self, db: Path) -> None:
        with pytest.raises(NoActiveTimerError):
            stop_timer(db)


class TestGetActiveTimer:
    """Tests for get_active_timer()."""

    def test_get_active_timer_when_running(self, db: Path) -> None:
        start_timer(db, description="active task")
        active = get_active_timer(db)
        assert active is not None
        assert active.description == "active task"

    def test_get_active_timer_when_idle(self, db: Path) -> None:
        active = get_active_timer(db)
        assert active is None

    def test_get_active_timer_after_stop(self, db: Path) -> None:
        start_timer(db, description="will stop")
        stop_timer(db)
        active = get_active_timer(db)
        assert active is None

    def test_start_after_stop_works(self, db: Path) -> None:
        start_timer(db, description="first")
        stop_timer(db)
        entry = start_timer(db, description="second")
        assert entry.description == "second"
        assert entry.end_time is None


class TestCreateProject:
    def test_create_project(self, db: Path) -> None:
        project = create_project(db, "my-project")
        assert project.name == "my-project"
        assert project.archived is False

    def test_create_duplicate_raises(self, db: Path) -> None:
        create_project(db, "dup-project")
        with pytest.raises(ProjectExistsError):
            create_project(db, "dup-project")

    def test_create_invalid_name_empty(self, db: Path) -> None:
        with pytest.raises(InvalidProjectNameError):
            create_project(db, "")

    def test_create_invalid_name_special_chars(self, db: Path) -> None:
        with pytest.raises(InvalidProjectNameError):
            create_project(db, "bad name!")

    def test_create_invalid_name_too_long(self, db: Path) -> None:
        with pytest.raises(InvalidProjectNameError):
            create_project(db, "a" * 51)


class TestListProjects:
    def test_list_includes_general(self, db: Path) -> None:
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "general" in names

    def test_list_includes_created(self, db: Path) -> None:
        create_project(db, "alpha")
        create_project(db, "beta")
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "alpha" in names
        assert "beta" in names

    def test_list_excludes_archived_by_default(self, db: Path) -> None:
        create_project(db, "to-archive")
        archive_project(db, "to-archive")
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "to-archive" not in names

    def test_list_includes_archived_when_requested(self, db: Path) -> None:
        create_project(db, "to-archive")
        archive_project(db, "to-archive")
        projects = list_projects(db, include_archived=True)
        names = [p.name for p in projects]
        assert "to-archive" in names


class TestArchiveProject:
    def test_archive_project(self, db: Path) -> None:
        create_project(db, "archivable")
        archive_project(db, "archivable")
        project = get_project(db, "archivable")
        assert project is not None
        assert project.archived is True

    def test_archive_nonexistent_raises(self, db: Path) -> None:
        with pytest.raises(ProjectNotFoundError):
            archive_project(db, "nonexistent")

    def test_archive_already_archived_raises(self, db: Path) -> None:
        create_project(db, "already")
        archive_project(db, "already")
        with pytest.raises(ProjectNotFoundError):
            archive_project(db, "already")

    def test_archive_general_raises(self, db: Path) -> None:
        with pytest.raises(ProjectNotFoundError):
            archive_project(db, "general")


class TestGetProject:
    def test_get_existing(self, db: Path) -> None:
        project = get_project(db, "general")
        assert project is not None
        assert project.name == "general"

    def test_get_nonexistent(self, db: Path) -> None:
        result = get_project(db, "nonexistent")
        assert result is None


def _insert_entry(db: Path, description: str, project: str, start: datetime, end: datetime, tags: str = "") -> None:
    """Helper to insert a completed entry directly into the DB."""
    conn = get_connection(db)
    try:
        conn.execute(
            "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (description, project, tags, start.isoformat(), end.isoformat(), start.isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


class TestReportDaily:
    """Tests for report_daily()."""

    def test_returns_entries_for_given_date(self, db: Path) -> None:
        today = date.today()
        start = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(today.year, today.month, today.day, 10, 30, tzinfo=timezone.utc)
        _insert_entry(db, "morning work", "general", start, end)

        entries = report_daily(db, today)
        assert len(entries) == 1
        assert entries[0].description == "morning work"

    def test_excludes_other_dates(self, db: Path) -> None:
        today = date.today()
        yesterday = today - timedelta(days=1)
        start_today = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end_today = datetime(today.year, today.month, today.day, 10, 0, tzinfo=timezone.utc)
        start_yest = datetime(yesterday.year, yesterday.month, yesterday.day, 9, 0, tzinfo=timezone.utc)
        end_yest = datetime(yesterday.year, yesterday.month, yesterday.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "today work", "general", start_today, end_today)
        _insert_entry(db, "yesterday work", "general", start_yest, end_yest)

        entries = report_daily(db, today)
        assert len(entries) == 1
        assert entries[0].description == "today work"

    def test_returns_empty_list_when_no_entries(self, db: Path) -> None:
        entries = report_daily(db, date.today())
        assert entries == []

    def test_includes_only_completed_entries(self, db: Path) -> None:
        today = date.today()
        start = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(today.year, today.month, today.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "completed", "general", start, end)
        # Start a timer but don't stop it (running entry)
        start_timer(db, description="running")

        entries = report_daily(db, today)
        assert len(entries) == 1
        assert entries[0].description == "completed"


class TestEditEntry:
    def test_edit_nonexistent_raises(self, db: Path) -> None:
        with pytest.raises(EntryNotFoundError):
            edit_entry(db, entry_id=9999)

    def test_edit_entry_description(self, db: Path) -> None:
        entry = start_timer(db, description="original")
        stop_timer(db)
        updated = edit_entry(db, entry_id=entry.id, description="updated")
        assert updated.description == "updated"


class TestDeleteEntry:
    def test_delete_nonexistent_raises(self, db: Path) -> None:
        with pytest.raises(EntryNotFoundError):
            delete_entry(db, entry_id=9999)

    def test_delete_entry(self, db: Path) -> None:
        entry = start_timer(db, description="to delete")
        stop_timer(db)
        delete_entry(db, entry_id=entry.id)
        with pytest.raises(EntryNotFoundError):
            edit_entry(db, entry_id=entry.id)


class TestReportWeekly:
    """Tests for report_weekly()."""

    def _get_monday(self) -> date:
        """Return the Monday of the current week."""
        today = date.today()
        return today - timedelta(days=today.weekday())

    def test_returns_per_project_summaries(self, db: Path) -> None:
        """report_weekly returns summaries with project, hours, percentage."""
        monday = self._get_monday()
        start1 = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end1 = datetime(monday.year, monday.month, monday.day, 11, 0, tzinfo=timezone.utc)
        _insert_entry(db, "work on general", "general", start1, end1)

        create_project(db, "webapp")
        start2 = datetime(monday.year, monday.month, monday.day, 13, 0, tzinfo=timezone.utc)
        end2 = datetime(monday.year, monday.month, monday.day, 14, 0, tzinfo=timezone.utc)
        _insert_entry(db, "work on webapp", "webapp", start2, end2)

        summaries = report_weekly(db)
class TestReportRange:
    """Tests for report_range()."""

    def test_returns_entries_within_range(self, db: Path) -> None:
        start1 = datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc)
        end1 = datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc)
        start2 = datetime(2024, 1, 20, 14, 0, tzinfo=timezone.utc)
        end2 = datetime(2024, 1, 20, 16, 0, tzinfo=timezone.utc)
        _insert_entry(db, "mid-month", "general", start1, end1)
        _insert_entry(db, "late-month", "general", start2, end2)

        entries = report_range(db, date(2024, 1, 1), date(2024, 1, 31))
        assert len(entries) == 2

    def test_excludes_entries_outside_range(self, db: Path) -> None:
        in_range = datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc)
        in_range_end = datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc)
        out_range = datetime(2024, 2, 5, 9, 0, tzinfo=timezone.utc)
        out_range_end = datetime(2024, 2, 5, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "in range", "general", in_range, in_range_end)
        _insert_entry(db, "out of range", "general", out_range, out_range_end)

        entries = report_range(db, date(2024, 1, 1), date(2024, 1, 31))
        assert len(entries) == 1
        assert entries[0].description == "in range"

    def test_returns_empty_for_no_entries(self, db: Path) -> None:
        entries = report_range(db, date(2024, 1, 1), date(2024, 1, 31))
        assert entries == []

    def test_excludes_running_entries(self, db: Path) -> None:
        today = date.today()
        start = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(today.year, today.month, today.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "completed", "general", start, end)
        start_timer(db, description="running")

        entries = report_range(db, today - timedelta(days=1), today + timedelta(days=1))
        assert len(entries) == 1
        assert entries[0].description == "completed"


class TestReportRangeSummary:
    """Tests for report_range_summary()."""

    def _get_monday(self) -> date:
        """Return the Monday of the current week."""
        today = date.today()
        return today - timedelta(days=today.weekday())

    def test_returns_per_project_summaries(self, db: Path) -> None:
        start1 = datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc)
        end1 = datetime(2024, 1, 15, 11, 0, tzinfo=timezone.utc)
        _insert_entry(db, "general work", "general", start1, end1)

        create_project(db, "webapp")
        start2 = datetime(2024, 1, 16, 9, 0, tzinfo=timezone.utc)
        end2 = datetime(2024, 1, 16, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "webapp work", "webapp", start2, end2)

        summaries = report_range_summary(db, date(2024, 1, 1), date(2024, 1, 31))
        assert len(summaries) == 2
        for s in summaries:
            assert "project" in s
            assert "hours" in s
            assert "percentage" in s

    def test_hours_calculated_correctly(self, db: Path) -> None:
        """Hours should be computed from entry durations."""
        monday = self._get_monday()
        start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(monday.year, monday.month, monday.day, 11, 30, tzinfo=timezone.utc)
        _insert_entry(db, "morning work", "general", start, end)

        summaries = report_weekly(db)
        assert len(summaries) == 1
        assert summaries[0]["project"] == "general"
        assert summaries[0]["hours"] == pytest.approx(2.5, abs=0.01)

    def test_percentage_calculated_correctly(self, db: Path) -> None:
        """Percentage = project hours / total hours * 100."""
        monday = self._get_monday()
        # general: 3 hours
        start1 = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end1 = datetime(monday.year, monday.month, monday.day, 12, 0, tzinfo=timezone.utc)
        _insert_entry(db, "general work", "general", start1, end1)

        # webapp: 1 hour
        create_project(db, "webapp")
        start2 = datetime(monday.year, monday.month, monday.day, 13, 0, tzinfo=timezone.utc)
        end2 = datetime(monday.year, monday.month, monday.day, 14, 0, tzinfo=timezone.utc)
        _insert_entry(db, "webapp work", "webapp", start2, end2)

        summaries = report_weekly(db)
        by_project = {s["project"]: s for s in summaries}
        assert by_project["general"]["percentage"] == pytest.approx(75.0, abs=0.1)
        assert by_project["webapp"]["percentage"] == pytest.approx(25.0, abs=0.1)

    def test_returns_empty_list_for_empty_week(self, db: Path) -> None:
        """Empty week returns empty list."""
        summaries = report_weekly(db)
        assert summaries == []

    def test_excludes_entries_outside_current_week(self, db: Path) -> None:
        """Entries from previous weeks are excluded."""
        monday = self._get_monday()
        last_week = monday - timedelta(days=7)
        start = datetime(last_week.year, last_week.month, last_week.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(last_week.year, last_week.month, last_week.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "old work", "general", start, end)

        summaries = report_weekly(db)
        assert summaries == []

    def test_excludes_running_entries(self, db: Path) -> None:
        """Running entries (no end_time) are excluded."""
        monday = self._get_monday()
        start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(monday.year, monday.month, monday.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "completed", "general", start, end)
        start_timer(db, description="running")

        summaries = report_weekly(db)
        assert len(summaries) == 1
        assert summaries[0]["hours"] == pytest.approx(1.0, abs=0.01)

    def test_returns_empty_for_no_entries(self, db: Path) -> None:
        summaries = report_range_summary(db, date(2024, 1, 1), date(2024, 1, 31))
        assert summaries == []

    def test_percentage_calculated_correctly(self, db: Path) -> None:
        # general: 3 hours, webapp: 1 hour -> 75% / 25%
        start1 = datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc)
        end1 = datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
        _insert_entry(db, "general", "general", start1, end1)

        create_project(db, "webapp")
        start2 = datetime(2024, 1, 16, 9, 0, tzinfo=timezone.utc)
        end2 = datetime(2024, 1, 16, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "webapp", "webapp", start2, end2)

        summaries = report_range_summary(db, date(2024, 1, 1), date(2024, 1, 31))
        by_proj = {s["project"]: s for s in summaries}
        assert by_proj["general"]["percentage"] == pytest.approx(75.0, abs=0.1)
        assert by_proj["webapp"]["percentage"] == pytest.approx(25.0, abs=0.1)
