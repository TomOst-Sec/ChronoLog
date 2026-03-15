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
