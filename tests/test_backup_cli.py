"""Tests for chrono db backup and chrono db restore CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from chronolog.cli import cli
from chronolog.core import start_timer, stop_timer
from chronolog.db import init_db


@pytest.fixture
def db(tmp_path: Path) -> Path:
    """Create and initialise a temporary database."""
    db_path = tmp_path / "backup_test.db"
    init_db(db_path)
    return db_path


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def populated_db(db: Path) -> Path:
    """Create a db with a completed entry."""
    entry = start_timer(db, description="test work", project="general")
    stop_timer(db)
    return db


class TestBackupCommand:
    """Tests for chrono db backup."""

    def test_backup_default_location(self, runner: CliRunner, populated_db: Path) -> None:
        """chrono db backup creates a backup in the default backups/ directory."""
        result = runner.invoke(cli, ["db", "backup", "--db", str(populated_db)])
        assert result.exit_code == 0
        assert "Backup" in result.output
        # Verify backup file was actually created
        backups_dir = populated_db.parent / "backups"
        assert backups_dir.exists()
        backup_files = list(backups_dir.glob("chrono_*.db"))
        assert len(backup_files) == 1

    def test_backup_custom_output(self, runner: CliRunner, populated_db: Path, tmp_path: Path) -> None:
        """chrono db backup --output /path creates backup at custom location."""
        output_path = tmp_path / "custom_backup.db"
        result = runner.invoke(cli, [
            "db", "backup",
            "--output", str(output_path),
            "--db", str(populated_db),
        ])
        assert result.exit_code == 0
        assert str(output_path) in result.output
        assert output_path.exists()

    def test_backup_shows_path_in_message(self, runner: CliRunner, populated_db: Path) -> None:
        """Success message includes the backup file path."""
        result = runner.invoke(cli, ["db", "backup", "--db", str(populated_db)])
        assert result.exit_code == 0
        # The output should contain a path ending in .db
        assert ".db" in result.output


class TestRestoreCommand:
    """Tests for chrono db restore."""

    def test_restore_with_confirmation(self, runner: CliRunner, populated_db: Path, tmp_path: Path) -> None:
        """chrono db restore prompts for confirmation and restores."""
        # Create a backup first
        from chronolog.backup import backup_db
        backup_path = backup_db(populated_db, tmp_path / "backup.db")

        result = runner.invoke(cli, [
            "db", "restore", str(backup_path),
            "--db", str(populated_db),
        ], input="y\n")
        assert result.exit_code == 0
        assert "Restored" in result.output

    def test_restore_fails_if_timer_running(self, runner: CliRunner, db: Path, tmp_path: Path) -> None:
        """Restore fails with clear error if a timer is running."""
        from chronolog.backup import backup_db
        backup_path = backup_db(db, tmp_path / "backup.db")

        # Start a timer (don't stop it)
        start_timer(db, description="still running")

        result = runner.invoke(cli, [
            "db", "restore", str(backup_path),
            "--yes",
            "--db", str(db),
        ])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_restore_fails_if_backup_missing(self, runner: CliRunner, db: Path) -> None:
        """Restore fails with clear error if backup file doesn't exist."""
        result = runner.invoke(cli, [
            "db", "restore", "/nonexistent/backup.db",
            "--yes",
            "--db", str(db),
        ])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_restore_with_yes_flag(self, runner: CliRunner, populated_db: Path, tmp_path: Path) -> None:
        """chrono db restore --yes skips confirmation."""
        from chronolog.backup import backup_db
        backup_path = backup_db(populated_db, tmp_path / "backup.db")

        result = runner.invoke(cli, [
            "db", "restore", str(backup_path),
            "--yes",
            "--db", str(populated_db),
        ])
        assert result.exit_code == 0
        assert "Restored" in result.output
        assert str(backup_path) in result.output

    def test_restore_aborted(self, runner: CliRunner, populated_db: Path, tmp_path: Path) -> None:
        """Declining confirmation aborts restore."""
        from chronolog.backup import backup_db
        backup_path = backup_db(populated_db, tmp_path / "backup.db")

        result = runner.invoke(cli, [
            "db", "restore", str(backup_path),
            "--db", str(populated_db),
        ], input="n\n")
        assert result.exit_code == 0
        assert "Aborted" in result.output
