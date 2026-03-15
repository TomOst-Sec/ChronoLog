"""Tests for the ChronoLog CLI."""

from click.testing import CliRunner

from chronolog import __version__
from chronolog.cli import cli


def test_version_flag():
    """chrono --version prints the correct version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help_flag():
    """chrono --help prints help text."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "ChronoLog" in result.output


def test_cli_group_no_args():
    """chrono with no arguments shows help."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
