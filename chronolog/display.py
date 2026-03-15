"""Rich formatting helpers for report output."""

from __future__ import annotations

from datetime import datetime, timezone

from rich.panel import Panel
from rich.table import Table

from chronolog.models import TimeEntry


def create_entries_table(entries: list[TimeEntry]) -> Table:
    """Create a Rich Table displaying time entries.

    Args:
        entries: List of TimeEntry objects to display.

    Returns:
        A Rich Table with columns: Start, End, Duration, Project, Tags, Description.
    """
    table = Table()
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Duration")
    table.add_column("Project")
    table.add_column("Tags")
    table.add_column("Description")

    for entry in entries:
        start_str = entry.start_time.strftime("%H:%M")

        if entry.end_time:
            end_str = entry.end_time.strftime("%H:%M")
            dur = entry.duration_minutes or 0.0
            dur_str = f"{dur:.1f}m"
        else:
            end_str = "[green]running[/green]"
            elapsed = datetime.now(timezone.utc) - entry.start_time
            dur_str = f"{elapsed.total_seconds() / 60:.1f}m"

        tags_str = ", ".join(entry.tags) if entry.tags else ""
        table.add_row(start_str, end_str, dur_str, entry.project, tags_str, entry.description)

    return table


def create_summary_table(summaries: list[dict]) -> Table:
    """Create a Rich Table for project summaries.

    Args:
        summaries: List of dicts with keys: project, hours, percentage.

    Returns:
        A Rich Table with columns: Project, Hours, Percentage, Bar.
    """
    table = Table()
    table.add_column("Project")
    table.add_column("Hours", justify="right")
    table.add_column("%", justify="right")
    table.add_column("Bar")

    for s in summaries:
        bar_width = int(s["percentage"] / 5)
        bar = "[green]" + "\u2588" * bar_width + "[/green]"
        table.add_row(
            s["project"],
            f"{s['hours']:.1f}",
            f"{s['percentage']:.0f}%",
            bar,
        )

    return table


def format_report_header(title: str, date_range: str) -> Panel:
    """Create a Rich Panel header for reports.

    Args:
        title: Report title.
        date_range: Date range description string.

    Returns:
        A Rich Panel with the title and date range.
    """
    return Panel(f"[bold]{title}[/bold]\n{date_range}")


def add_total_row(table: Table, total_minutes: float) -> None:
    """Add a bold total row at the bottom of a table.

    Args:
        table: The Rich Table to add the total row to.
        total_minutes: Total duration in minutes.
    """
    hours = total_minutes / 60
    table.add_section()
    table.add_row(
        "",
        "",
        f"[bold]{total_minutes:.1f}m ({hours:.1f}h)[/bold]",
        "",
        "",
        "[bold]Total[/bold]",
    )
