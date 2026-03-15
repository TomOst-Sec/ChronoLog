"""Tests for chrono edit and chrono delete CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from chronolog.cli import cli
from chronolog.core import start_timer, stop_timer
from chronolog.db import init_db


@pytest.fixture
def db(tmp_path: Path) -> Path:
    """Create and initialise a temporary database."""
    db_path = tmp_path / "edit_delete.db"
    init_db(db_path)
    return db_path


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def stopped_entry(db: Path):
    """Create a stopped entry and return it."""
    entry = start_timer(db, description="original desc", project="general", tags=["old"])
    return stop_timer(db)


class TestEditCommand:
    """Tests for chrono edit ID."""

    def test_edit_description(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono edit ID --description 'new desc' updates the description."""
        result = runner.invoke(cli, [
            "edit", str(stopped_entry.id),
            "--description", "new desc",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "new desc" in result.output

    def test_edit_project(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono edit ID --project new-project updates the project."""
        # Create the target project first
        runner.invoke(cli, ["project", "create", "new-project"])
        # For testing we need to use db-aware project creation
        from chronolog.core import create_project
        create_project(db, "new-project")

        result = runner.invoke(cli, [
            "edit", str(stopped_entry.id),
            "--project", "new-project",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "new-project" in result.output

    def test_edit_tags(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono edit ID --tags 'tag1,tag2' updates the tags."""
        result = runner.invoke(cli, [
            "edit", str(stopped_entry.id),
            "--tags", "tag1,tag2",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "tag1" in result.output

    def test_edit_multiple_flags(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """Multiple edit flags can be combined in one command."""
        result = runner.invoke(cli, [
            "edit", str(stopped_entry.id),
            "--description", "updated",
            "--tags", "newtag",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "updated" in result.output
        assert "newtag" in result.output

    def test_edit_nonexistent_entry(self, runner: CliRunner, db: Path) -> None:
        """chrono edit with invalid ID shows error."""
        result = runner.invoke(cli, [
            "edit", "9999",
            "--description", "nope",
            "--db", str(db),
        ])
        assert result.exit_code == 1
        assert "Error" in result.output


class TestDeleteCommand:
    """Tests for chrono delete ID."""

    def test_delete_with_confirmation(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono delete ID prompts for confirmation and deletes."""
        result = runner.invoke(cli, [
            "delete", str(stopped_entry.id),
            "--db", str(db),
        ], input="y\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_delete_with_yes_flag(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono delete ID --yes skips confirmation."""
        result = runner.invoke(cli, [
            "delete", str(stopped_entry.id),
            "--yes",
            "--db", str(db),
        ])
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_delete_nonexistent_entry(self, runner: CliRunner, db: Path) -> None:
        """chrono delete with invalid ID shows error."""
        result = runner.invoke(cli, [
            "delete", "9999",
            "--yes",
            "--db", str(db),
        ])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_delete_aborted(self, runner: CliRunner, db: Path, stopped_entry) -> None:
        """chrono delete ID with 'n' confirmation aborts."""
        result = runner.invoke(cli, [
            "delete", str(stopped_entry.id),
            "--db", str(db),
        ], input="n\n")
        assert result.exit_code == 0
        assert "Aborted" in result.output
