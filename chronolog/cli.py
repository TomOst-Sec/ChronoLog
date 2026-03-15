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
    start_timer,
    stop_timer,
)
from chronolog.db import get_db_path, init_db

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
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
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
    except RuntimeError as exc:
        console.print("[red]Error:[/red] No timer is currently running")
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
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
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
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
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
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
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
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


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
