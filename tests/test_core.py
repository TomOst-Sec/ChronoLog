"""Tests for ChronoLog core business logic."""

from pathlib import Path

import pytest

from chronolog.core import get_active_timer, start_timer, stop_timer
from chronolog.db import init_db


@pytest.fixture
def db(tmp_db_path: Path) -> Path:
    """Return an initialised temporary database path."""
    init_db(tmp_db_path)
    return tmp_db_path


class TestStartTimer:
    """Tests for start_timer()."""

    def test_start_timer_basic(self, db: Path) -> None:
        entry = start_timer(db, description="writing code")
        assert entry.description == "writing code"
        assert entry.project == "general"
        assert entry.tags == []
        assert entry.end_time is None
        assert entry.id is not None
        assert entry.start_time.tzinfo is not None

    def test_start_timer_with_project_and_tags(self, db: Path) -> None:
        entry = start_timer(
            db,
            description="feature work",
            project="general",
            tags=["dev", "feature"],
        )
        assert entry.project == "general"
        assert entry.tags == ["dev", "feature"]

    def test_start_timer_raises_if_already_running(self, db: Path) -> None:
        start_timer(db, description="first")
        with pytest.raises(Exception, match="already"):
            start_timer(db, description="second")

    def test_start_timer_raises_if_project_missing(self, db: Path) -> None:
        with pytest.raises(Exception, match="project"):
            start_timer(db, description="task", project="nonexistent")


class TestStopTimer:
    """Tests for stop_timer()."""

    def test_stop_timer(self, db: Path) -> None:
        start_timer(db, description="to stop")
        stopped = stop_timer(db)
        assert stopped.description == "to stop"
        assert stopped.end_time is not None
        assert stopped.end_time >= stopped.start_time

    def test_stop_timer_raises_if_none_running(self, db: Path) -> None:
        with pytest.raises(Exception, match="[Nn]o.*running|not running"):
            stop_timer(db)


class TestGetActiveTimer:
    """Tests for get_active_timer()."""

    def test_get_active_timer_when_running(self, db: Path) -> None:
        start_timer(db, description="active task")
        active = get_active_timer(db)
        assert active is not None
        assert active.description == "active task"

    def test_get_active_timer_when_idle(self, db: Path) -> None:
        active = get_active_timer(db)
        assert active is None

    def test_get_active_timer_after_stop(self, db: Path) -> None:
        start_timer(db, description="will stop")
        stop_timer(db)
        active = get_active_timer(db)
        assert active is None

    def test_start_after_stop_works(self, db: Path) -> None:
        start_timer(db, description="first")
        stop_timer(db)
        entry = start_timer(db, description="second")
        assert entry.description == "second"
        assert entry.end_time is None
