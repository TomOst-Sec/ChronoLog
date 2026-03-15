"""Database backup and restore for ChronoLog."""

import shutil
from datetime import datetime
from pathlib import Path

from chronolog.db import get_connection


def backup_db(db_path: Path, output_path: Path | None = None) -> Path:
    """Create a backup of the database file.

    Args:
        db_path: Path to the active database.
        output_path: Custom backup destination. If None, backs up to
            the default backups/ directory with a timestamped filename.

    Returns:
        Path to the created backup file.
    """
    if output_path is None:
        backups_dir = db_path.parent / "backups"
        backups_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = backups_dir / f"chrono_{timestamp}.db"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(str(db_path), str(output_path))
    return output_path


def restore_db(db_path: Path, backup_path: Path) -> None:
    """Restore the database from a backup file.

    Args:
        db_path: Path to the active database to overwrite.
        backup_path: Path to the backup file to restore from.

    Raises:
        RuntimeError: If a timer is currently running.
        FileNotFoundError: If the backup file doesn't exist.
    """
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_path}")

    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT id FROM entries WHERE end_time IS NULL").fetchone()
        if row is not None:
            raise RuntimeError("A timer is currently running — stop it before restoring.")
    finally:
        conn.close()

    shutil.copy2(str(backup_path), str(db_path))
