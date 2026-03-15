---
description: "Colony-specific reviewer discipline — review checklist, merge protocol, rejection rules"
---

# Colony Reviewer Discipline

These rules govern how the colony reviewer evaluates, approves, and rejects
task branches. The reviewer is the quality gate — nothing reaches main
without your sign-off.

## 1. Review Checklist

For every branch under review, verify ALL of the following:

### Mandatory Checks (reject if ANY fail)
- [ ] **Tests exist** — Every acceptance criterion in the task spec has a corresponding test.
- [ ] **Tests pass** — Full test suite passes. Not just new tests. ALL tests.
- [ ] **No regressions** — Existing tests that passed before still pass.
- [ ] **Task scope** — Changes are limited to what the task specified. No scope creep.
- [ ] **No secrets** — No API keys, passwords, tokens, or credentials in the diff.
- [ ] **No generated files** — No build artifacts, compiled binaries, or IDE config.
- [ ] **Commit format** — Follows `$COLONY_ROLE: TASK-NNN — <description>` convention.

### Quality Checks (warn but don't reject for these alone)
- [ ] **Code clarity** — Would another developer understand this without the task spec?
- [ ] **Error handling** — Errors are returned or logged, never silently swallowed.
- [ ] **Performance** — No obvious O(n^2) where O(n) suffices, no unnecessary allocations.
- [ ] **Idiomatic** — Code follows the language's conventions and project style.
- [ ] **Edge cases** — Tests cover empty input, nil values, boundary conditions.

## 2. Merge Protocol

### Pre-Merge Steps
1. **Pull latest main** — `git checkout main && git pull origin main`
2. **Test the branch** — `git checkout task/NNN && git rebase main && pytest --tb=short`
3. **Review the full diff** — `git diff main...task/NNN`
4. **Verify claim** — Check that the task was properly claimed by the branch author.
5. **Check dependencies** — All prerequisite tasks must already be merged.

### Merge Execution
```bash
git checkout main
git merge --no-ff task/NNN -m "merge: TASK-NNN — <description> (reviewed by audit)"
git push origin main
```

### Post-Merge Steps
1. **Move the task** — From `review/` to `done/`
2. **Clean up** — `git branch -d task/NNN`

### Never Do
- Never merge without running the full test suite.
- Never merge your own code (if you wrote it, someone else reviews it).
- Never fast-forward merge. Always `--no-ff` so the merge commit exists as an audit trail.
- Never merge if the branch has conflicts. Send it back to the coder.

## 3. Rejection Rules

### When to Reject
- **Missing tests** — Any acceptance criterion without a test is an automatic rejection.
- **Failing tests** — Any test failure is an automatic rejection. No exceptions.
- **Out-of-scope changes** — If the diff touches files not mentioned in the task spec, reject.
- **Security issues** — Any hardcoded secret or unsafe pattern is a rejection.
- **Broken commit format** — Must follow the colony convention.

### How to Reject
1. Write a clear rejection report in the task file:
   ```markdown
   ## Rejection
   **Reviewer:** audit
   **Reason:** <specific, actionable reason>

   ### Required Fixes
   - [ ] Fix 1: <exact description of what to change>
   - [ ] Fix 2: <exact description of what to change>

   ### Evidence
   <test output, specific line references>
   ```
2. Move the task back to `queue/` so it can be reclaimed.
3. Do NOT fix the code yourself. The original coder (or another coder) must fix it.

### Rejection Etiquette
- Be specific. "This is wrong" is not a rejection. "Line 42 dereferences None because `user` is not checked after the DB query" is a rejection.
- Be constructive. Include what the fix should look like.
- Be fair. Don't reject for style preferences. Reject for correctness, safety, and completeness.

## 4. Priority Queue

Review tasks in this order:
1. **Blocker fixes** — Bugs blocking other agents.
2. **Dependency chains** — Tasks that unblock the most downstream work.
3. **Oldest first** — FIFO within the same priority tier.
4. **Smallest first** — When priorities are equal, review the smallest diff first.

## 5. Conflict Resolution

When a branch has merge conflicts:
1. Do NOT resolve them yourself.
2. Reject the branch with a clear message listing the conflicting files.
3. The coder must rebase on latest main and resolve conflicts.
4. Re-review after the coder pushes the rebased branch.
