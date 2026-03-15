"""Click CLI entry points for ChronoLog."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from chronolog import __version__
from chronolog.config import get_config, set_config
from chronolog.core import (
    archive_project,
    create_project,
    delete_entry,
    edit_entry,
    get_active_timer,
    list_entries,
    list_projects,
    list_tags,
    report_daily,
    report_weekly,
    start_timer,
    stop_timer,
)
from chronolog.db import get_db_path, init_db
from chronolog.display import add_total_row, create_entries_table, create_summary_table
from chronolog.exceptions import ChronoLogError

console = Console()


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="chrono")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """ChronoLog — track your time from the command line."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("description")
@click.option("--project", "-p", default="general", help="Project name.")
@click.option("--tags", "-t", default="", help="Comma-separated tags.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def start(description: str, project: str, tags: str, db: str | None) -> None:
    """Start a new timer."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    try:
        entry = start_timer(db_path, description=description, project=project, tags=tag_list)
        console.print(f"[green]Started:[/green] {entry.description}")
        console.print(f"  Project: {entry.project}")
        if entry.tags:
            console.print(f"  Tags: {', '.join(entry.tags)}")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        raise SystemExit(1)


@cli.command()
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def stop(db: str | None) -> None:
    """Stop the running timer."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    try:
        entry = stop_timer(db_path)
        console.print(f"[green]Stopped:[/green] {entry.description}")
        console.print(f"  Project: {entry.project}")
        if entry.duration_minutes is not None:
            console.print(f"  Duration: {entry.duration_minutes:.1f} minutes")
        if entry.tags:
            console.print(f"  Tags: {', '.join(entry.tags)}")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        raise SystemExit(1)


@cli.command()
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def status(db: str | None) -> None:
    """Show the currently running timer."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    entry = get_active_timer(db_path)
    if entry is None:
        console.print("[yellow]No timer running[/yellow]")
        return
    from datetime import datetime, timezone

    elapsed = datetime.now(timezone.utc) - entry.start_time
    minutes = elapsed.total_seconds() / 60.0
    console.print(f"[green]Running:[/green] {entry.description}")
    console.print(f"  Project: {entry.project}")
    console.print(f"  Elapsed: {minutes:.1f} minutes")
    if entry.tags:
        console.print(f"  Tags: {', '.join(entry.tags)}")




@cli.command()
@click.argument("entry_id", type=int)
@click.option("--description", "-d", default=None, help="New description.")
@click.option("--project", "-p", default=None, help="New project name.")
@click.option("--tags", "-t", default=None, help="New comma-separated tags.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def edit(entry_id: int, description: str | None, project: str | None, tags: str | None, db: str | None) -> None:
    """Edit an existing time entry."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    try:
        entry = edit_entry(db_path, entry_id, description=description, project=project, tags=tag_list)
        console.print(f"[green]Updated:[/green] {entry.description}")
        console.print(f"  Project: {entry.project}")
        if entry.tags:
            console.print(f"  Tags: {', '.join(entry.tags)}")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        raise SystemExit(1)


@cli.command()
@click.argument("entry_id", type=int)
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def delete(entry_id: int, yes: bool, db: str | None) -> None:
    """Delete a time entry."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    if not yes:
        if not click.confirm(f"Delete entry {entry_id}?"):
            console.print("[yellow]Aborted.[/yellow]")
            return
    try:
        delete_entry(db_path, entry_id)
        console.print(f"[green]Deleted:[/green] entry {entry_id}")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        raise SystemExit(1)


@cli.command("list")
@click.option("--limit", "-n", default=10, help="Number of entries to show.")
@click.option("--db", type=click.Path(), default=None, hidden=True)
def list_cmd(limit: int, db: str | None) -> None:
    """Show recent time entries."""
    from pathlib import Path as P
    db_path = P(db) if db else get_db_path()
    entries = list_entries(db_path, limit=limit)
    if not entries:
        console.print("[dim]No entries yet.[/dim]")
        return
    table = Table(title="Recent Entries")
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Description")
    table.add_column("Project", style="cyan")
    table.add_column("Start")
    table.add_column("Duration", justify="right")
    for entry in entries:
        dur = entry.duration
        if dur is not None:
            mins = int(dur.total_seconds() / 60)
            duration_str = f"{mins}m"
        else:
            from datetime import datetime, timezone
            elapsed = datetime.now(timezone.utc) - entry.start_time
            mins = int(elapsed.total_seconds() / 60)
            duration_str = f"{mins}m (running)"
        table.add_row(
            str(entry.id),
            entry.description,
            entry.project,
            entry.start_time.strftime("%Y-%m-%d %H:%M"),
            duration_str,
        )
    console.print(table)

@cli.group(invoke_without_command=True)
@click.pass_context
def project(ctx: click.Context) -> None:
    """Manage projects."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@project.command("create")
@click.argument("name")
def project_create(name: str) -> None:
    """Create a new project."""
    db_path = get_db_path()
    try:
        proj = create_project(db_path, name)
        console.print(f"[green]Created project '{proj.name}'.[/green]")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        sys.exit(1)


@project.command("list")
@click.option("--all", "include_all", is_flag=True, help="Include archived projects.")
def project_list(include_all: bool) -> None:
    """List projects."""
    db_path = get_db_path()
    projects = list_projects(db_path, include_archived=include_all)
    table = Table(title="Projects")
    table.add_column("Name")
    table.add_column("Created")
    if include_all:
        table.add_column("Status")
    for proj in projects:
        row = [proj.name, proj.created_at.strftime("%Y-%m-%d %H:%M")]
        if include_all:
            row.append("archived" if proj.archived else "active")
        table.add_row(*row)
    console.print(table)


@project.command("archive")
@click.argument("name")
def project_archive(name: str) -> None:
    """Archive a project."""
    db_path = get_db_path()
    try:
        archive_project(db_path, name)
        console.print(f"[yellow]Archived project '{name}'.[/yellow]")
    except ChronoLogError as exc:
        console.print(f"[red]Error:[/red] {exc.message}")
        sys.exit(1)


@cli.group("db")
def db_group() -> None:
    """Database backup and restore."""


@db_group.command("backup")
@click.option("--output", "-o", default=None, type=click.Path(), help="Custom backup file path.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def db_backup(output: str | None, db: str | None) -> None:
    """Create a database backup."""
    from chronolog.backup import backup_db

    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    output_path = Path(output) if output else None
    result = backup_db(db_path, output_path)
    console.print(f"[green]Backup created:[/green] {result}")


@db_group.command("restore")
@click.argument("backup_file", type=click.Path())
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def db_restore(backup_file: str, yes: bool, db: str | None) -> None:
    """Restore the database from a backup file."""
    from chronolog.backup import restore_db

    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    backup_path = Path(backup_file)
    if not yes:
        if not click.confirm(f"Restore database from {backup_path}?"):
            console.print("[yellow]Aborted.[/yellow]")
            return
    try:
        restore_db(db_path, backup_path)
        console.print(f"[green]Restored:[/green] database from {backup_path}")
    except (ChronoLogError, RuntimeError, FileNotFoundError) as exc:
        msg = exc.message if isinstance(exc, ChronoLogError) else str(exc)
        console.print(f"[red]Error:[/red] {msg}")
        raise SystemExit(1)


@cli.group()
def config() -> None:
    """Manage ChronoLog configuration."""


@config.command("show")
@click.option("--config-path", type=click.Path(), default=None, hidden=True)
def config_show(config_path: str | None) -> None:
    """Display current configuration settings."""
    path = Path(config_path) if config_path else None
    cfg = get_config(config_path=path)
    table = Table(title="ChronoLog Configuration")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    for key, value in cfg.items():
        table.add_row(key, str(value))
    console.print(table)


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--config-path", type=click.Path(), default=None, hidden=True)
def config_set(key: str, value: str, config_path: str | None) -> None:
    """Set a configuration value."""
    path = Path(config_path) if config_path else None
    set_config(key, value, config_path=path)
    click.echo(f"Set {key} = {value}")


@cli.group(invoke_without_command=True)
@click.pass_context
def report(ctx: click.Context) -> None:
    """View time reports."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@report.command("today")
@click.option("--db", type=click.Path(), default=None, hidden=True)
def report_today(db: str | None) -> None:
    """Show today's time entries."""
    from datetime import date

    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    target = date.today()
    entries = report_daily(db_path, target)
    if not entries:
        console.print(f"[dim]No entries for {target.isoformat()}[/dim]")
        return
    table = create_entries_table(entries)
    total_minutes = sum(e.duration_minutes or 0.0 for e in entries)
    add_total_row(table, total_minutes)
    console.print(table)


@report.command("yesterday")
@click.option("--db", type=click.Path(), default=None, hidden=True)
def report_yesterday(db: str | None) -> None:
    """Show yesterday's time entries."""
    from datetime import date, timedelta

    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    target = date.today() - timedelta(days=1)
    entries = report_daily(db_path, target)
    if not entries:
        console.print(f"[dim]No entries for {target.isoformat()}[/dim]")
        return
    table = create_entries_table(entries)
    total_minutes = sum(e.duration_minutes or 0.0 for e in entries)
    add_total_row(table, total_minutes)
    console.print(table)


@report.command("week")
@click.option("--db", type=click.Path(), default=None, hidden=True)
def report_week(db: str | None) -> None:
    """Show weekly summary by project."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    summaries = report_weekly(db_path)
    if not summaries:
        console.print("[dim]No entries for this week[/dim]")
        return
    table = create_summary_table(summaries)
    total_hours = sum(s["hours"] for s in summaries)
    table.add_section()
    table.add_row("[bold]Total[/bold]", f"[bold]{total_hours:.1f}[/bold]", "", "")
    console.print(table)


@cli.command("export")
@click.option("--from", "from_date", required=True, help="Start date (YYYY-MM-DD).")
@click.option("--to", "to_date", required=True, help="End date (YYYY-MM-DD).")
@click.option("--output", "-o", default=None, type=click.Path(), help="Output file path. Defaults to stdout.")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def export_cmd(from_date: str, to_date: str, output: str | None, db: str | None) -> None:
    """Export time entries to CSV."""
    import re
    from chronolog.export import export_entries_csv

    db_path = Path(db) if db else get_db_path()
    init_db(db_path)

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for label, value in [("--from", from_date), ("--to", to_date)]:
        if not date_pattern.match(value):
            console.print(f"[red]Error:[/red] Invalid date format for {label}: '{value}'. Use YYYY-MM-DD.")
            raise SystemExit(1)

    output_path = Path(output) if output else None
    export_entries_csv(db_path, from_date, to_date, output_path)

    from chronolog.db import get_connection
    conn = get_connection(db_path)
    try:
        count = conn.execute(
            """SELECT COUNT(*) FROM entries
               WHERE end_time IS NOT NULL
                 AND date(start_time) >= date(?)
                 AND date(start_time) <= date(?)""",
            (from_date, to_date),
        ).fetchone()[0]
    finally:
        conn.close()

    dest = str(output_path) if output_path else "stdout"
    console.print(f"[green]Exported {count} entries to {dest}[/green]")


def _format_minutes(total_minutes: float) -> str:
    """Format minutes as 'Xh Ym' or 'Xm'.

    Args:
        total_minutes: Total minutes to format.

    Returns:
        A human-readable time string.
    """
    minutes = int(total_minutes)
    if minutes >= 60:
        hours = minutes // 60
        remaining = minutes % 60
        return f"{hours}h {remaining}m"
    return f"{minutes}m"


@cli.command("tags")
@click.option("--db", type=click.Path(), default=None, hidden=True, help="Database path (for testing).")
def tags_cmd(db: str | None) -> None:
    """List all tags with total time."""
    db_path = Path(db) if db else get_db_path()
    init_db(db_path)
    tag_data = list_tags(db_path)
    if not tag_data:
        console.print("[dim]No tags found[/dim]")
        return
    table = Table(title="Tags")
    table.add_column("Tag", style="cyan")
    table.add_column("Total Time", justify="right")
    table.add_column("Entries", justify="right")
    for entry in tag_data:
        table.add_row(
            entry["tag"],
            _format_minutes(entry["total_minutes"]),
            str(entry["entry_count"]),
        )
    console.print(table)
