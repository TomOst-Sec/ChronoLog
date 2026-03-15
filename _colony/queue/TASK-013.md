# TASK-013: Error handling and custom exceptions

**Status:** queue
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001

## Description
Define custom exception classes for ChronoLog and ensure all core functions raise descriptive errors. Clean error messages improve both the CLI user experience and debugging. This centralizes error types that are currently ad-hoc strings/ValueError.

## Acceptance Criteria
- [ ] Module `chronolog/exceptions.py` with custom exception classes:
  - `ChronoLogError` (base class)
  - `TimerAlreadyRunningError` — raised when starting a timer while one is active
  - `NoActiveTimerError` — raised when stopping/checking status with no active timer
  - `ProjectNotFoundError` — raised when referencing a non-existent project
  - `ProjectExistsError` — raised when creating a duplicate project
  - `EntryNotFoundError` — raised when editing/deleting a non-existent entry
  - `InvalidProjectNameError` — raised when project name fails validation
- [ ] All exception classes include a user-friendly `message` attribute
- [ ] Core functions (`start_timer`, `stop_timer`, `create_project`, etc.) use these exceptions instead of generic ValueError/RuntimeError
- [ ] CLI commands catch `ChronoLogError` subclasses and display the message with Rich formatting (red text, no traceback)
- [ ] Tests verifying each exception is raised in the correct scenario
- [ ] At least 7 test cases

## Notes
- Keep exceptions simple — inherit from `ChronoLogError` which inherits from `Exception`
- Each exception class needs just `__init__(self, message: str)` calling `super().__init__(message)`
- Update existing core.py code to use new exceptions (coordinate with whatever is merged)
