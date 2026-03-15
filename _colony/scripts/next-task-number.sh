#!/bin/bash
set -euo pipefail
COLONY_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAX=0
for dir in queue active review done; do
  for f in "$COLONY_ROOT/$dir"/TASK-*.md; do
    [ -f "$f" ] || continue
    NUM=$(basename "$f" .md | sed 's/TASK-//')
    NUM=$((10#$NUM))
    [ "$NUM" -gt "$MAX" ] && MAX=$NUM
  done
done
printf "TASK-%03d\n" $((MAX + 1))
