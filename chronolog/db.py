"""SQLite database initialization and connection management for ChronoLog."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def get_db_path(base_dir: Path | None = None) -> Path:
    """Return the database file path, creating the parent directory if needed.

    Args:
        base_dir: Override the default ~/.chronolog directory. If None,
            uses ~/.chronolog.

    Returns:
        Path to the chrono.db file.
    """
    if base_dir is None:
        base_dir = Path.home() / ".chronolog"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "chrono.db"


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection with Row factory enabled.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        A sqlite3.Connection with row_factory set to sqlite3.Row.
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    """Initialize the database schema and default data.

    Creates the entries and projects tables if they don't exist,
    and inserts the default 'general' project. Safe to call multiple times.

    Args:
        db_path: Path to the SQLite database file.
    """
    conn = get_connection(db_path)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                project TEXT NOT NULL DEFAULT 'general',
                tags TEXT DEFAULT '',
                start_time TEXT NOT NULL,
                end_time TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                name TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                archived INTEGER DEFAULT 0
            )
        """)
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "INSERT OR IGNORE INTO projects (name, created_at, archived) VALUES (?, ?, 0)",
            ("general", now),
        )
        conn.commit()
    finally:
        conn.close()
