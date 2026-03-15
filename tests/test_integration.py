"""End-to-end integration tests for ChronoLog M1 workflow."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from chronolog.cli import cli
from chronolog.core import get_active_timer, start_timer, stop_timer
from chronolog.db import get_connection, init_db


@pytest.fixture
def db(tmp_path: Path) -> Path:
    """Create and initialise a temporary database."""
    db_path = tmp_path / "integration.db"
    init_db(db_path)
    return db_path


@pytest.fixture
def runner() -> CliRunner:
    """Return a Click CliRunner."""
    return CliRunner()


class TestTimerWorkflow:
    """Full timer lifecycle: start -> status -> stop -> verify."""

    def test_full_timer_lifecycle(self, db: Path) -> None:
        """Start a timer, check active, stop it, verify it completed."""
        entry = start_timer(db, description="writing tests")

        assert entry.id is not None
        assert entry.description == "writing tests"
        assert entry.project == "general"
        assert entry.end_time is None

        active = get_active_timer(db)
        assert active is not None
        assert active.id == entry.id
        assert active.description == "writing tests"

        stopped = stop_timer(db)
        assert stopped.id == entry.id
        assert stopped.end_time is not None
        assert stopped.duration is not None
        assert stopped.duration.total_seconds() >= 0

        assert get_active_timer(db) is None

    def test_completed_entry_persists_in_db(self, db: Path) -> None:
        """After stop, the entry is in the DB with correct data."""
        start_timer(db, description="persistent check")
        stopped = stop_timer(db)

        conn = get_connection(db)
        try:
            row = conn.execute(
                "SELECT * FROM entries WHERE id = ?", (stopped.id,)
            ).fetchone()
            assert row is not None
            assert row["description"] == "persistent check"
            assert row["project"] == "general"
            assert row["end_time"] is not None
        finally:
            conn.close()


class TestProjectWorkflow:
    """Create project, start timer with project, verify."""

    def test_start_timer_with_custom_project(self, db: Path) -> None:
        """Create a project, start a timer on it, stop, verify entry."""
        conn = get_connection(db)
        try:
            from datetime import datetime, timezone

            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO projects (name, created_at, archived) VALUES (?, ?, 0)",
                ("myproject", now),
            )
            conn.commit()
        finally:
            conn.close()

        entry = start_timer(db, description="project work", project="myproject")
        assert entry.project == "myproject"

        stopped = stop_timer(db)
        assert stopped.project == "myproject"

        conn = get_connection(db)
        try:
            row = conn.execute(
                "SELECT * FROM entries WHERE id = ?", (stopped.id,)
            ).fetchone()
            assert row["project"] == "myproject"
        finally:
            conn.close()


class TestErrorCases:
    """Error conditions: start while running, stop while idle, bad project."""

    def test_start_while_running_raises(self, db: Path) -> None:
        """Cannot start a second timer while one is active."""
        start_timer(db, description="first")
        with pytest.raises(RuntimeError, match="already running"):
            start_timer(db, description="second")

    def test_stop_while_idle_raises(self, db: Path) -> None:
        """Cannot stop when no timer is running."""
        with pytest.raises(RuntimeError, match="No timer is currently running"):
            stop_timer(db)

    def test_start_with_nonexistent_project_raises(self, db: Path) -> None:
        """Cannot start a timer with a project that doesn't exist."""
        with pytest.raises(RuntimeError, match="No such project"):
            start_timer(db, description="bad project", project="nonexistent")


class TestDefaultProject:
    """Timer without explicit project uses 'general'."""

    def test_default_project_is_general(self, db: Path) -> None:
        """Starting without --project defaults to general."""
        entry = start_timer(db, description="default project test")
        assert entry.project == "general"

        stopped = stop_timer(db)
        assert stopped.project == "general"


class TestTagsWorkflow:
    """Tags round-trip through start -> stop -> DB."""

    def test_tags_persist_through_workflow(self, db: Path) -> None:
        """Start with tags, stop, verify tags in DB and returned entry."""
        entry = start_timer(
            db, description="tagged work", tags=["bug", "urgent"]
        )
        assert entry.tags == ["bug", "urgent"]

        active = get_active_timer(db)
        assert active is not None
        assert active.tags == ["bug", "urgent"]

        stopped = stop_timer(db)
        assert stopped.tags == ["bug", "urgent"]

        conn = get_connection(db)
        try:
            row = conn.execute(
                "SELECT tags FROM entries WHERE id = ?", (stopped.id,)
            ).fetchone()
            assert row["tags"] == "bug,urgent"
        finally:
            conn.close()

    def test_empty_tags_workflow(self, db: Path) -> None:
        """Timer with no tags stores empty string in DB."""
        start_timer(db, description="no tags")
        stopped = stop_timer(db)

        conn = get_connection(db)
        try:
            row = conn.execute(
                "SELECT tags FROM entries WHERE id = ?", (stopped.id,)
            ).fetchone()
            assert row["tags"] == ""
        finally:
            conn.close()


class TestCLIIntegration:
    """CLI-level tests using CliRunner for available commands."""

    def test_version_outputs_correctly(self, runner: CliRunner) -> None:
        """chrono --version shows version string."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help_shows_group_info(self, runner: CliRunner) -> None:
        """chrono --help shows the CLI group description."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "ChronoLog" in result.output
