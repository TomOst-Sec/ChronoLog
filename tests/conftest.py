"""Shared fixtures for ChronoLog tests."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_db_path(tmp_path: Path) -> Path:
    """Return a temporary database path for testing."""
    return tmp_path / "test_chrono.db"
