# TASK-039: Project color coding for Rich output

**Status:** queue
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Assign colors to projects for consistent Rich terminal output. Each project gets a stable color so entries are visually distinguishable in reports and lists.

## Acceptance Criteria
- [ ] Function `get_project_color(project_name: str) -> str` returns a Rich color name based on project name hash
- [ ] Color palette of 8-10 distinct terminal colors that work on dark and light backgrounds
- [ ] Same project always maps to same color (deterministic via hash)
- [ ] Colors applied to project column in `chrono list`, `chrono report`, and `chrono tags` output
- [ ] "general" project gets a neutral/default color
- [ ] Tests: deterministic color mapping, all projects get valid colors, general project color
- [ ] At least 4 test cases

## Notes
- Use `hash(project_name) % len(colors)` for consistent mapping
- Rich color names: "cyan", "green", "yellow", "magenta", "blue", "red", "white", "bright_black"
- Keep it simple — no user-configurable colors
