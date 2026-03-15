---
description: "Colony-specific coder discipline — task claiming, worktree hygiene, commit conventions, when-stuck protocol"
---

# Colony Coder Discipline

These rules are specific to AtlasColony multi-agent coordination. They
supplement the general coding skills with colony-aware workflows.

## 1. Task Claiming Protocol

Before starting any work:

1. **Check the task queue** — `_colony/queue/`
2. **Claim the task** — Run `_colony/scripts/claim-task.sh TASK-NNN.md $COLONY_ROLE`
3. **Verify the claim succeeded** — If it fails, another agent grabbed it first. Pick a different task.
4. **Never work without a claim.** Unclaimed work creates merge conflicts and wasted effort.

### Claim Etiquette
- Claim ONE task at a time. Finish or release it before claiming another.
- If you've been working on a task for >30 minutes without progress, release it.
- Never steal a task claimed by another agent. If their claim is stale, let the overseer handle it.

## 2. Worktree Hygiene

Every task runs in an isolated git worktree. No exceptions.

### Creation
```bash
INSTANCE="$COLONY_ROLE"          # e.g., alpha-1
TASK="NNN"                       # task number

git worktree add .worktrees/${INSTANCE}-task-${TASK} -b task/${TASK} main
cd .worktrees/${INSTANCE}-task-${TASK}
```

### Maintenance
- Install dependencies immediately after creating the worktree.
- Run baseline tests BEFORE writing any code. If they fail, stop and report.
- Do NOT modify files outside your task's scope.
- Do NOT commit generated files, build artifacts, or IDE config.

### Cleanup
After a task is pushed and complete:
```bash
cd "$COLONY_DIR"
git worktree remove .worktrees/${INSTANCE}-task-${TASK} --force
git branch -d task/${TASK} 2>/dev/null || true
```
Always clean up. Abandoned worktrees waste disk and confuse other agents.

## 3. Commit Conventions

### Format
```
$COLONY_ROLE: TASK-NNN — <concise description>

<optional body explaining WHY, not WHAT>
```

### Rules
- One logical change per commit. Don't bundle unrelated changes.
- The description must be understandable without reading the diff.
- Reference the task number in every commit.
- Never force-push. Never rewrite shared history.
- Sign off on your commit: the `$COLONY_ROLE` prefix IS your signature.

### Examples
```
alpha-1: TASK-042 — add rate limiter to API gateway
alpha-2: TASK-017 — fix nil pointer in user lookup
bravo-1: TASK-099 — add integration tests for payment flow
```

## 4. When-Stuck Protocol

If you are stuck — genuinely stuck, not "I haven't tried hard enough" stuck:

### Tier 1: Self-Help (first 5-10 minutes)
- Re-read the task spec. You probably missed something.
- Re-read the error message. The answer is often right there.
- Check if a dependency task was merged. Maybe you're missing upstream changes.
- `git pull origin main --rebase` — maybe the fix is already in.

### Tier 2: Structured Debugging (next 10-15 minutes)
- Isolate the problem. Can you reproduce it in a minimal test?
- Add logging at every step. Where does actual diverge from expected?
- Check related tests for examples of correct usage.
- Read the function signatures — are you passing the right types?

### Tier 3: Escalate (after 15-20 minutes of genuine effort)
- Write a bug report in `_colony/queue/` as a new task.
- Include: root cause hypothesis, what you tried, exact error output.
- Move the task back to queue if you can't complete it.
- Pick a different task. Do NOT keep spinning on the same problem.

### What NOT To Do When Stuck
- Do NOT silently skip tests to make them pass.
- Do NOT comment out failing code.
- Do NOT commit broken code hoping the reviewer will fix it.
- Do NOT spend more than 30 minutes total on a single blocker.
- Do NOT ask other agents for help directly — use the bug queue.

## 5. Branch Protection Awareness

- The `main` branch is protected. You cannot push directly to it.
- All work goes through task branches: `task/NNN`
- The reviewer merges approved branches. You push; they merge.
- If your branch has conflicts with main, rebase locally before pushing.
