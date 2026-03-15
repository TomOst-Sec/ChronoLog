"""Custom exception classes for ChronoLog."""


class ChronoLogError(Exception):
    """Base exception for all ChronoLog errors.

    Args:
        message: A user-friendly error message.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class TimerAlreadyRunningError(ChronoLogError):
    """Raised when starting a timer while one is already active."""


class NoActiveTimerError(ChronoLogError):
    """Raised when stopping or checking status with no active timer."""


class ProjectNotFoundError(ChronoLogError):
    """Raised when referencing a non-existent project."""


class ProjectExistsError(ChronoLogError):
    """Raised when creating a duplicate project."""


class EntryNotFoundError(ChronoLogError):
    """Raised when editing or deleting a non-existent time entry."""


class InvalidProjectNameError(ChronoLogError):
    """Raised when a project name fails validation."""
