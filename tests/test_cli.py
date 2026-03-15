"""Tests for the ChronoLog CLI."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from chronolog import __version__
from chronolog.cli import cli
from chronolog.db import get_connection, init_db


@pytest.fixture
def db(tmp_db_path: Path) -> Path:
    """Return an initialised temporary database path."""
    init_db(tmp_db_path)
    return tmp_db_path


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


def test_version_flag():
    """chrono --version prints the correct version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help_flag():
    """chrono --help prints help text."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "ChronoLog" in result.output


def test_cli_group_no_args():
    """chrono with no arguments shows help."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0


class TestReportTodayCLI:
    """Tests for chrono report today."""

    def test_report_today_shows_entries(self, db: Path) -> None:
        today = date.today()
        start = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(today.year, today.month, today.day, 10, 30, tzinfo=timezone.utc)
        _insert_entry(db, "morning coding", "general", start, end)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "today", "--db", str(db)])
        assert result.exit_code == 0
        assert "morning coding" in result.output

    def test_report_today_shows_total(self, db: Path) -> None:
        today = date.today()
        start = datetime(today.year, today.month, today.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(today.year, today.month, today.day, 10, 0, tzinfo=timezone.utc)
        _insert_entry(db, "work", "general", start, end)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "today", "--db", str(db)])
        assert result.exit_code == 0
        assert "Total" in result.output

    def test_report_today_empty(self, db: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "today", "--db", str(db)])
        assert result.exit_code == 0
        assert "No entries for" in result.output


class TestReportYesterdayCLI:
    """Tests for chrono report yesterday."""

    def test_report_yesterday_shows_entries(self, db: Path) -> None:
        yesterday = date.today() - timedelta(days=1)
        start = datetime(yesterday.year, yesterday.month, yesterday.day, 14, 0, tzinfo=timezone.utc)
        end = datetime(yesterday.year, yesterday.month, yesterday.day, 16, 0, tzinfo=timezone.utc)
        _insert_entry(db, "afternoon work", "general", start, end)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "yesterday", "--db", str(db)])
        assert result.exit_code == 0
        assert "afternoon work" in result.output

    def test_report_yesterday_empty(self, db: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "yesterday", "--db", str(db)])
        assert result.exit_code == 0
        assert "No entries for" in result.output


class TestTagsCommand:
    """Tests for chrono tags CLI command."""

    def test_tags_displays_table_with_tag_data(self, db: Path) -> None:
        """chrono tags shows a Rich table with tag, total time, entries."""
        now = datetime.now(timezone.utc)
        conn = get_connection(db)
        try:
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("task1", "general", "bug,urgent",
                 (now - timedelta(hours=2, minutes=30)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("task2", "general", "bug",
                 (now - timedelta(minutes=45)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        runner = CliRunner()
        result = runner.invoke(cli, ["tags", "--db", str(db)])
        assert result.exit_code == 0
        assert "bug" in result.output
        assert "urgent" in result.output
        assert "Tag" in result.output
        assert "Total Time" in result.output
        assert "Entries" in result.output

    def test_tags_formats_time_as_hours_and_minutes(self, db: Path) -> None:
        """Tags with >= 60 min show 'Xh Ym' format."""
        now = datetime.now(timezone.utc)
        conn = get_connection(db)
        try:
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("long task", "general", "dev",
                 (now - timedelta(hours=2, minutes=30)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        runner = CliRunner()
        result = runner.invoke(cli, ["tags", "--db", str(db)])
        assert result.exit_code == 0
        assert "2h 30m" in result.output

    def test_tags_formats_short_time_as_minutes(self, db: Path) -> None:
        """Tags with < 60 min show 'Xm' format."""
        now = datetime.now(timezone.utc)
        conn = get_connection(db)
        try:
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("short task", "general", "quick",
                 (now - timedelta(minutes=25)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        runner = CliRunner()
        result = runner.invoke(cli, ["tags", "--db", str(db)])
        assert result.exit_code == 0
        assert "25m" in result.output

    def test_tags_empty_shows_no_tags_message(self, db: Path) -> None:
        """chrono tags with no tags shows a friendly message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["tags", "--db", str(db)])
        assert result.exit_code == 0
        assert "No tags found" in result.output

    def test_tags_sorted_by_total_time_descending(self, db: Path) -> None:
        """Tags are sorted by total time, highest first."""
        now = datetime.now(timezone.utc)
        conn = get_connection(db)
        try:
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("big task", "general", "dev",
                 (now - timedelta(hours=3)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.execute(
                "INSERT INTO entries (description, project, tags, start_time, end_time, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("small task", "general", "bug",
                 (now - timedelta(minutes=30)).isoformat(),
                 now.isoformat(), now.isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

        runner = CliRunner()
        result = runner.invoke(cli, ["tags", "--db", str(db)])
        assert result.exit_code == 0
        dev_pos = result.output.index("dev")
        bug_pos = result.output.index("bug")
        assert dev_pos < bug_pos


class TestReportWeekCLI:
    """Tests for chrono report week."""

    def _get_monday(self) -> date:
        today = date.today()
        return today - timedelta(days=today.weekday())

    def test_report_week_shows_summary_table(self, db: Path) -> None:
        """chrono report week shows project summary with bar chart."""
        monday = self._get_monday()
        start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(monday.year, monday.month, monday.day, 12, 0, tzinfo=timezone.utc)
        _insert_entry(db, "general work", "general", start, end)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "week", "--db", str(db)])
        assert result.exit_code == 0
        assert "general" in result.output
        assert "Project" in result.output
        assert "Hours" in result.output

    def test_report_week_shows_total_hours(self, db: Path) -> None:
        """Total hours shown at bottom."""
        monday = self._get_monday()
        start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=timezone.utc)
        end = datetime(monday.year, monday.month, monday.day, 11, 0, tzinfo=timezone.utc)
        _insert_entry(db, "work", "general", start, end)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "week", "--db", str(db)])
        assert result.exit_code == 0
        assert "Total" in result.output
        assert "2.0" in result.output

    def test_report_week_empty_shows_message(self, db: Path) -> None:
        """Empty week shows a friendly message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "week", "--db", str(db)])
        assert result.exit_code == 0
        assert "No entries" in result.output
class TestReportRangeCLI:
    """Tests for chrono report --from/--to CLI command."""

    def test_detail_view_by_default(self, db: Path) -> None:
        """chrono report --from X --to Y shows detail entries."""
        _insert_entry(
            db, "jan work", "general",
            datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc),
        )
        runner = CliRunner()
        result = runner.invoke(cli, [
            "report", "--from", "2024-01-01", "--to", "2024-01-31",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "jan work" in result.output

    def test_summary_view_with_flag(self, db: Path) -> None:
        """chrono report --from X --to Y --summary shows project summary."""
        _insert_entry(
            db, "project work", "general",
            datetime(2024, 1, 15, 9, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc),
        )
        runner = CliRunner()
        result = runner.invoke(cli, [
            "report", "--from", "2024-01-01", "--to", "2024-01-31",
            "--summary", "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "general" in result.output
        assert "Project" in result.output

    def test_empty_range_shows_message(self, db: Path) -> None:
        """Empty range shows a friendly message."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "report", "--from", "2024-01-01", "--to", "2024-01-31",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "No entries" in result.output

    def test_invalid_date_format_shows_error(self, db: Path) -> None:
        """Invalid date format shows clear error."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "report", "--from", "01-01-2024", "--to", "2024-01-31",
            "--db", str(db),
        ])
        assert result.exit_code == 1
        assert "Invalid date format" in result.output

    def test_from_and_to_both_required(self, db: Path) -> None:
        """Using --from without --to shows an error."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            "report", "--from", "2024-01-01", "--db", str(db),
        ])
        assert result.exit_code != 0
