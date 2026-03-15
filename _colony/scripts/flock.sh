#!/usr/bin/env bash
# AtlasColony — flock-based atomic queue operations
# Source this file: source "$COLONY_DIR/lib/flock.sh"
#
# Provides filesystem-level locking via flock(1) to eliminate race conditions
# when multiple colony instances claim or complete tasks concurrently.

# Resolve COLONY_DIR if not already set
COLONY_DIR="${COLONY_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

# Lock directory — excluded from git via .gitignore
LOCK_DIR="_colony/locks"

# ── with_lock() ──────────────────────────────────────────────────────────────
# Execute a function under an exclusive flock with a 10-second timeout.
#
# Usage: with_lock <lock_name> <command> [args...]
#   lock_name: arbitrary string used to derive the lock file
#   command:   function or command to run while holding the lock
#
# Returns the exit code of the wrapped command.
# Returns 1 if the lock cannot be acquired within 10 seconds.
with_lock() {
  local lock_name="${1:?Usage: with_lock <lock_name> <command> [args...]}"
  shift

  mkdir -p "$LOCK_DIR"
  local lockfile="$LOCK_DIR/${lock_name}.lock"

  (
    if ! flock -w 10 9; then
      echo "ERROR: Could not acquire lock '$lock_name' within 10 seconds" >&2
      return 1
    fi
    "$@"
  ) 9>"$lockfile"
}

# ── _do_atomic_move() ────────────────────────────────────────────────────────
# Internal: validates source exists, destination doesn't, performs mv,
# and appends Claimed-By / Claimed-At metadata to the moved file.
#
# Usage: _do_atomic_move <from_dir> <to_dir> <task_file> <instance>
#
# Exit 0 = moved successfully
# Exit 1 = source missing or destination already exists
_do_atomic_move() {
  local from_dir="$1"
  local to_dir="$2"
  local task_file="$3"
  local instance="$4"

  local src="_colony/${from_dir}/${task_file}"
  local dst="_colony/${to_dir}/${task_file}"

  # Validate source exists
  if [ ! -f "$src" ]; then
    echo "ERROR: $task_file not found in ${from_dir}/ — already moved or does not exist" >&2
    return 1
  fi

  # Validate destination does not already exist
  if [ -f "$dst" ]; then
    echo "ERROR: $task_file already exists in ${to_dir}/ — refusing to overwrite" >&2
    return 1
  fi

  # Ensure destination directory exists
  mkdir -p "_colony/${to_dir}"

  # Atomic move
  mv "$src" "$dst"

  # Append claim metadata
  printf '\n**Claimed-By:** %s\n**Claimed-At:** %s\n' \
    "$instance" \
    "$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')" \
    >> "$dst"
}

# ── atomic_move() ────────────────────────────────────────────────────────────
# Atomic task state transition using flock-based locking.
#
# Usage: atomic_move <from_dir> <to_dir> <task_file> <instance>
#   from_dir:  source queue directory name (e.g., "queue", "active")
#   to_dir:    destination directory name (e.g., "active", "review")
#   task_file: task filename (e.g., "TASK-001.md")
#   instance:  claiming instance name (e.g., "alpha-1")
#
# Acquires an exclusive lock keyed on the task filename before moving,
# ensuring only one instance can transition a given task at a time.
atomic_move() {
  local from_dir="${1:?Usage: atomic_move <from_dir> <to_dir> <task_file> <instance>}"
  local to_dir="${2:?Usage: atomic_move <from_dir> <to_dir> <task_file> <instance>}"
  local task_file="${3:?Usage: atomic_move <from_dir> <to_dir> <task_file> <instance>}"
  local instance="${4:?Usage: atomic_move <from_dir> <to_dir> <task_file> <instance>}"

  with_lock "$task_file" _do_atomic_move "$from_dir" "$to_dir" "$task_file" "$instance"
}
