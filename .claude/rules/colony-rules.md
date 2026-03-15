# Colony Rules (enforced for all agents)

## 1. Stay In Your Lane
- Read `$COLONY_ROLE` at session start. That is your identity for this entire session.
- Only perform actions listed under your role in `_colony/SYSTEM.md`.
- If your role says "never writes code," you do not write code. Period.
- If your role says "never merges," you do not merge. Period.

## 2. Use The Scripts
- Claim tasks with `_colony/scripts/claim-task.sh TASK-NNN.md $COLONY_ROLE`
- Complete tasks with `_colony/scripts/complete-task.sh TASK-NNN.md $COLONY_ROLE`
- Get next task number with `_colony/scripts/next-task-number.sh`
- Do NOT manually move files between queue/active/review/done.

## 3. Run Tests Before Everything
- Before writing code: run `pytest` to confirm baseline passes.
- Before pushing: run `pytest` to confirm nothing broke.
- If tests fail before you touched anything, STOP and file a bug.

## 4. Commit Format
```
<instance>: TASK-NNN -- <description>
```
Examples:
- `alpha-1: TASK-042 -- add rate limiter to API gateway`
- `audit: merge TASK-042 -- add rate limiter (reviewed by audit)`
- `atlas: TASK-043 -- generated new task for auth module`

## 5. Team Boundaries
- alpha-1, alpha-2, alpha-3: only claim tasks with `Assigned: alpha`
- bravo-1, bravo-2: only claim tasks with `Assigned: bravo`
- Never claim a task assigned to the other team.

## 6. Git Hygiene
- Always `git pull origin main --rebase` before starting work.
- Never force push.
- Never push directly to main (only audit does this via merge).
- Use worktrees for task branches. Clean them up when done.

## 7. Check PAUSE
- At the start of every cycle, check if `_colony/PAUSE` exists.
- If it does, stop immediately. Do not start new work.

## 8. Task Lifecycle
```
queue/ --> active/ --> review/ --> done/
                                    |
                         rejected --+--> queue/ (with bug notes)
```
- Tasks only move forward through the pipeline.
- Rejected tasks go back to queue with rejection notes appended.

## 9. No Secrets
- Never commit API keys, passwords, tokens, or credentials.
- Never commit `.env` files.
- If you find a secret in the codebase, file a P0 bug immediately.

## 10. Python Standards
- Use pytest for all tests.
- Use Click for CLI commands.
- Use Rich for terminal output.
- Absolute imports only.
- Type hints on all public functions.
- Google-style docstrings on all public functions.
