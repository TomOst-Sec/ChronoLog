"""Tests for the database layer."""

import sqlite3
from pathlib import Path

import pytest

from chronolog.db import get_connection, get_db_path, init_db


class TestGetDbPath:
    """Tests for get_db_path()."""

    def test_returns_expected_path(self) -> None:
        """Default path is ~/.chronolog/chrono.db."""
        path = get_db_path()
        assert path == Path.home() / ".chronolog" / "chrono.db"

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        """Parent directory is created if it doesn't exist."""
        db_dir = tmp_path / "subdir"
        path = get_db_path(base_dir=db_dir)
        assert path == db_dir / "chrono.db"
        assert db_dir.exists()


class TestGetConnection:
    """Tests for get_connection()."""

    def test_returns_connection_with_row_factory(self, tmp_db_path: Path) -> None:
        """Connection has sqlite3.Row as row_factory."""
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        assert conn.row_factory is sqlite3.Row
        conn.close()

    def test_connection_is_usable(self, tmp_db_path: Path) -> None:
        """Connection can execute queries."""
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        cursor = conn.execute("SELECT 1 AS val")
        row = cursor.fetchone()
        assert row["val"] == 1
        conn.close()


class TestInitDb:
    """Tests for init_db()."""

    def test_creates_entries_table(self, tmp_db_path: Path) -> None:
        """init_db creates the entries table with correct schema."""
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='entries'"
        )
        row = cursor.fetchone()
        assert row is not None
        schema = row["sql"].lower()
        assert "id integer primary key autoincrement" in schema
        assert "description text not null" in schema
        assert "project text not null" in schema
        assert "start_time text not null" in schema
        assert "end_time text" in schema
        assert "created_at text not null" in schema
        conn.close()

    def test_creates_projects_table(self, tmp_db_path: Path) -> None:
        """init_db creates the projects table with correct schema."""
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='projects'"
        )
        row = cursor.fetchone()
        assert row is not None
        schema = row["sql"].lower()
        assert "name text primary key" in schema
        assert "created_at text not null" in schema
        assert "archived integer default 0" in schema
        conn.close()

    def test_inserts_default_general_project(self, tmp_db_path: Path) -> None:
        """init_db creates a default 'general' project."""
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        cursor = conn.execute(
            "SELECT name, archived FROM projects WHERE name = 'general'"
        )
        row = cursor.fetchone()
        assert row is not None
        assert row["name"] == "general"
        assert row["archived"] == 0
        conn.close()

    def test_is_idempotent(self, tmp_db_path: Path) -> None:
        """Calling init_db multiple times does not raise or duplicate data."""
        init_db(tmp_db_path)
        init_db(tmp_db_path)
        init_db(tmp_db_path)
        conn = get_connection(tmp_db_path)
        cursor = conn.execute("SELECT COUNT(*) AS cnt FROM projects WHERE name = 'general'")
        row = cursor.fetchone()
        assert row["cnt"] == 1
        conn.close()

    def test_creates_database_file(self, tmp_db_path: Path) -> None:
        """init_db creates the database file on disk."""
        assert not tmp_db_path.exists()
        init_db(tmp_db_path)
        assert tmp_db_path.exists()
