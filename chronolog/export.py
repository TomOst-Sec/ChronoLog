"""CSV export functionality for ChronoLog."""

import csv
import sys
from datetime import datetime
from pathlib import Path
from typing import IO

from chronolog.db import get_connection, init_db

CSV_COLUMNS = [
    "date", "start_time", "end_time", "duration_minutes",
    "project", "tags", "description",
]


def export_entries_csv(
    db_path: Path,
    from_date: str,
    to_date: str,
    output_path: Path | None = None,
) -> None:
    """Export time entries to CSV format.

    Queries completed entries within the date range and writes them
    as CSV. Running entries (no end_time) are excluded.

    Args:
        db_path: Path to the SQLite database.
        from_date: Start date in YYYY-MM-DD format (inclusive).
        to_date: End date in YYYY-MM-DD format (inclusive).
        output_path: Path to write CSV file. If None, writes to stdout.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """SELECT description, project, tags, start_time, end_time
               FROM entries
               WHERE end_time IS NOT NULL
                 AND date(start_time) >= date(?)
                 AND date(start_time) <= date(?)
               ORDER BY start_time""",
            (from_date, to_date),
        ).fetchall()
    finally:
        conn.close()

    if output_path is not None:
        with open(output_path, "w", newline="") as f:
            _write_csv(f, rows)
    else:
        _write_csv(sys.stdout, rows)


def _write_csv(f: IO[str], rows: list) -> None:
    """Write entry rows as CSV to a file object.

    Args:
        f: File-like object to write to.
        rows: List of sqlite3.Row objects from the entries query.
    """
    writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for row in rows:
        start = datetime.fromisoformat(row["start_time"])
        end = datetime.fromisoformat(row["end_time"])
        local_start = start.astimezone()
        local_end = end.astimezone()
        duration = (end - start).total_seconds() / 60.0

        writer.writerow({
            "date": local_start.strftime("%Y-%m-%d"),
            "start_time": local_start.strftime("%H:%M"),
            "end_time": local_end.strftime("%H:%M"),
            "duration_minutes": f"{duration:.1f}",
            "project": row["project"],
            "tags": row["tags"],
            "description": row["description"],
        })
