"""Tests for ChronoLog data models."""

from datetime import datetime, timedelta, timezone

from chronolog.models import Project, TimeEntry


class TestTimeEntryCreation:
    """Test TimeEntry dataclass creation."""

    def test_create_time_entry_with_all_fields(self) -> None:
        now = datetime.now(timezone.utc)
        entry = TimeEntry(
            id=1,
            description="working on feature",
            project="myproject",
            tags=["dev", "feature"],
            start_time=now,
            end_time=now + timedelta(hours=1),
        )
        assert entry.id == 1
        assert entry.description == "working on feature"
        assert entry.project == "myproject"
        assert entry.tags == ["dev", "feature"]
        assert entry.start_time == now
        assert entry.end_time == now + timedelta(hours=1)

    def test_create_running_entry_no_end_time(self) -> None:
        now = datetime.now(timezone.utc)
        entry = TimeEntry(
            id=None,
            description="still running",
            project="general",
            tags=[],
            start_time=now,
            end_time=None,
        )
        assert entry.id is None
        assert entry.end_time is None


class TestTimeEntryDuration:
    """Test duration property calculations."""

    def test_duration_completed_entry(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 11, 30, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="done",
            project="general",
            tags=[],
            start_time=start,
            end_time=end,
        )
        assert entry.duration == timedelta(hours=1, minutes=30)

    def test_duration_running_entry_returns_none(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="running",
            project="general",
            tags=[],
            start_time=start,
            end_time=None,
        )
        assert entry.duration is None

    def test_duration_minutes_completed_entry(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 11, 30, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="done",
            project="general",
            tags=[],
            start_time=start,
            end_time=end,
        )
        assert entry.duration_minutes == 90.0

    def test_duration_minutes_running_entry_returns_none(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="running",
            project="general",
            tags=[],
            start_time=start,
            end_time=None,
        )
        assert entry.duration_minutes is None


class TestTimeEntrySerialisation:
    """Test to_row / from_row round-trip."""

    def test_to_row_returns_dict_with_tags_as_string(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="task",
            project="proj",
            tags=["a", "b", "c"],
            start_time=start,
            end_time=end,
        )
        row = entry.to_row()
        assert isinstance(row, dict)
        assert row["tags"] == "a,b,c"
        assert row["description"] == "task"
        assert row["project"] == "proj"
        assert row["start_time"] == start.isoformat()
        assert row["end_time"] == end.isoformat()

    def test_to_row_empty_tags(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        entry = TimeEntry(
            id=1,
            description="task",
            project="proj",
            tags=[],
            start_time=start,
            end_time=None,
        )
        row = entry.to_row()
        assert row["tags"] == ""
        assert row["end_time"] is None

    def test_from_row_reconstructs_entry(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        row = {
            "id": 5,
            "description": "roundtrip",
            "project": "proj",
            "tags": "x,y",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }
        entry = TimeEntry.from_row(row)
        assert entry.id == 5
        assert entry.tags == ["x", "y"]
        assert entry.start_time == start
        assert entry.end_time == end

    def test_from_row_empty_tags_string(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        row = {
            "id": 6,
            "description": "no tags",
            "project": "proj",
            "tags": "",
            "start_time": start.isoformat(),
            "end_time": None,
        }
        entry = TimeEntry.from_row(row)
        assert entry.tags == []
        assert entry.end_time is None

    def test_roundtrip_to_row_from_row(self) -> None:
        start = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        original = TimeEntry(
            id=10,
            description="round trip test",
            project="dev",
            tags=["tag1", "tag2"],
            start_time=start,
            end_time=end,
        )
        row = original.to_row()
        row["id"] = original.id
        restored = TimeEntry.from_row(row)
        assert restored.id == original.id
        assert restored.description == original.description
        assert restored.project == original.project
        assert restored.tags == original.tags
        assert restored.start_time == original.start_time
        assert restored.end_time == original.end_time


class TestProject:
    """Test Project dataclass."""

    def test_create_project(self) -> None:
        now = datetime.now(timezone.utc)
        p = Project(name="myproject", created_at=now)
        assert p.name == "myproject"
        assert p.created_at == now
        assert p.archived is False

    def test_create_archived_project(self) -> None:
        now = datetime.now(timezone.utc)
        p = Project(name="old", created_at=now, archived=True)
        assert p.archived is True
