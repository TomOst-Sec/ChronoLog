"""Tests for ChronoLog core business logic."""

from pathlib import Path

import pytest

from chronolog.core import (
    archive_project,
    create_project,
    get_active_timer,
    get_project,
    list_projects,
    start_timer,
    stop_timer,
)
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


class TestCreateProject:
    def test_create_project(self, db: Path) -> None:
        project = create_project(db, "my-project")
        assert project.name == "my-project"
        assert project.archived is False

    def test_create_duplicate_raises(self, db: Path) -> None:
        create_project(db, "dup-project")
        with pytest.raises(ValueError, match="already exists"):
            create_project(db, "dup-project")

    def test_create_invalid_name_empty(self, db: Path) -> None:
        with pytest.raises(ValueError, match="invalid"):
            create_project(db, "")

    def test_create_invalid_name_special_chars(self, db: Path) -> None:
        with pytest.raises(ValueError, match="invalid"):
            create_project(db, "bad name!")

    def test_create_invalid_name_too_long(self, db: Path) -> None:
        with pytest.raises(ValueError, match="invalid"):
            create_project(db, "a" * 51)


class TestListProjects:
    def test_list_includes_general(self, db: Path) -> None:
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "general" in names

    def test_list_includes_created(self, db: Path) -> None:
        create_project(db, "alpha")
        create_project(db, "beta")
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "alpha" in names
        assert "beta" in names

    def test_list_excludes_archived_by_default(self, db: Path) -> None:
        create_project(db, "to-archive")
        archive_project(db, "to-archive")
        projects = list_projects(db)
        names = [p.name for p in projects]
        assert "to-archive" not in names

    def test_list_includes_archived_when_requested(self, db: Path) -> None:
        create_project(db, "to-archive")
        archive_project(db, "to-archive")
        projects = list_projects(db, include_archived=True)
        names = [p.name for p in projects]
        assert "to-archive" in names


class TestArchiveProject:
    def test_archive_project(self, db: Path) -> None:
        create_project(db, "archivable")
        archive_project(db, "archivable")
        project = get_project(db, "archivable")
        assert project is not None
        assert project.archived is True

    def test_archive_nonexistent_raises(self, db: Path) -> None:
        with pytest.raises(ValueError, match="does not exist"):
            archive_project(db, "nonexistent")

    def test_archive_already_archived_raises(self, db: Path) -> None:
        create_project(db, "already")
        archive_project(db, "already")
        with pytest.raises(ValueError, match="already archived"):
            archive_project(db, "already")

    def test_archive_general_raises(self, db: Path) -> None:
        with pytest.raises(ValueError, match="general"):
            archive_project(db, "general")


class TestGetProject:
    def test_get_existing(self, db: Path) -> None:
        project = get_project(db, "general")
        assert project is not None
        assert project.name == "general"

    def test_get_nonexistent(self, db: Path) -> None:
        result = get_project(db, "nonexistent")
        assert result is None
