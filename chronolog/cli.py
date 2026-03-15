"""Click CLI entry points for ChronoLog."""

import click

from chronolog import __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="chrono")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """ChronoLog — track your time from the command line."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
