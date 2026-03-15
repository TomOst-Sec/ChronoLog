"""Tests for ChronoLog custom exceptions."""

import pytest

from chronolog.exceptions import (
    ChronoLogError,
    TimerAlreadyRunningError,
    NoActiveTimerError,
    ProjectNotFoundError,
    ProjectExistsError,
    EntryNotFoundError,
    InvalidProjectNameError,
)


class TestExceptionHierarchy:
    def test_base_inherits_from_exception(self):
        assert issubclass(ChronoLogError, Exception)

    def test_timer_already_running_inherits(self):
        assert issubclass(TimerAlreadyRunningError, ChronoLogError)

    def test_no_active_timer_inherits(self):
        assert issubclass(NoActiveTimerError, ChronoLogError)

    def test_project_not_found_inherits(self):
        assert issubclass(ProjectNotFoundError, ChronoLogError)

    def test_project_exists_inherits(self):
        assert issubclass(ProjectExistsError, ChronoLogError)

    def test_entry_not_found_inherits(self):
        assert issubclass(EntryNotFoundError, ChronoLogError)

    def test_invalid_project_name_inherits(self):
        assert issubclass(InvalidProjectNameError, ChronoLogError)


class TestExceptionMessages:
    def test_chronolog_error_message(self):
        err = ChronoLogError("something failed")
        assert str(err) == "something failed"
        assert err.message == "something failed"

    def test_timer_already_running_message(self):
        err = TimerAlreadyRunningError("Timer is already running")
        assert "already running" in str(err)
        assert err.message == "Timer is already running"

    def test_no_active_timer_message(self):
        err = NoActiveTimerError("No timer is running")
        assert "No timer" in str(err)

    def test_project_not_found_message(self):
        err = ProjectNotFoundError("Project 'foo' not found")
        assert "foo" in str(err)

    def test_project_exists_message(self):
        err = ProjectExistsError("Project 'bar' already exists")
        assert "bar" in str(err)

    def test_entry_not_found_message(self):
        err = EntryNotFoundError("Entry 42 not found")
        assert "42" in str(err)

    def test_invalid_project_name_message(self):
        err = InvalidProjectNameError("Name '!!!' is invalid")
        assert "invalid" in str(err).lower()


class TestExceptionCatching:
    def test_catch_as_chronolog_error(self):
        with pytest.raises(ChronoLogError):
            raise TimerAlreadyRunningError("test")

    def test_catch_as_chronolog_error_project(self):
        with pytest.raises(ChronoLogError):
            raise ProjectNotFoundError("test")

    def test_catch_specific_type(self):
        with pytest.raises(NoActiveTimerError):
            raise NoActiveTimerError("no timer")
