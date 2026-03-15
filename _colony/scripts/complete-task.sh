#!/bin/bash
set -euo pipefail
TASK="${1:?Usage: complete-task.sh TASK-NNN.md <instance>}"
INSTANCE="${2:?Usage: complete-task.sh TASK-NNN.md <instance>}"
cd "$(git rev-parse --show-toplevel)"
if [ ! -f "_colony/active/$TASK" ]; then echo "ERROR: $TASK not in active"; exit 1; fi
mv "_colony/active/$TASK" "_colony/review/$TASK"
sed -i "s/Status:.*/Status:** review/" "_colony/review/$TASK" 2>/dev/null || true
printf '\n**Completed-At:** %s\n' "$(date +%s)" >> "_colony/review/$TASK"
git add "_colony/active/$TASK" "_colony/review/$TASK"
git commit -m "$INSTANCE: completed $TASK — moved to review"
git push origin main || { git reset --soft HEAD~1; exit 1; }
echo "OK: $TASK moved to review"
