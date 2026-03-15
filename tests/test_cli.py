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


class TestProjectDbOption:
    """Tests for --db option on project subcommands."""

    def test_project_create_with_db_option(self, tmp_path):
        """chrono project create NAME --db PATH uses the specified database."""
        db_path = tmp_path / "test.db"
        init_db(db_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["project", "create", "myproject", "--db", str(db_path)])
        assert result.exit_code == 0
        assert "myproject" in result.output

        # Verify the project was actually created in the right db
        conn = get_connection(db_path)
        try:
            row = conn.execute("SELECT name FROM projects WHERE name = 'myproject'").fetchone()
            assert row is not None
        finally:
            conn.close()

    def test_project_list_with_db_option(self, tmp_path):
        """chrono project list --db PATH reads from the specified database."""
        db_path = tmp_path / "test.db"
        init_db(db_path)
        runner = CliRunner()
        result = runner.invoke(cli, ["project", "list", "--db", str(db_path)])
        assert result.exit_code == 0
        assert "general" in result.output

    def test_project_archive_with_db_option(self, tmp_path):
        """chrono project archive NAME --db PATH uses the specified database."""
        db_path = tmp_path / "test.db"
        init_db(db_path)
        # First create a project to archive
        conn = get_connection(db_path)
        try:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("INSERT OR IGNORE INTO projects (name, created_at, archived) VALUES (?, ?, 0)", ("testproj", now))
            conn.commit()
        finally:
            conn.close()

        runner = CliRunner()
        result = runner.invoke(cli, ["project", "archive", "testproj", "--db", str(db_path)])
        assert result.exit_code == 0
        assert "testproj" in result.output
