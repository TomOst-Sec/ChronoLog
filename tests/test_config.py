"""Tests for ChronoLog configuration system."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from chronolog.config import get_config, set_config, DEFAULT_CONFIG
from chronolog.cli import cli


@pytest.fixture
def tmp_config_path(tmp_path: Path) -> Path:
    """Return a temporary config file path for testing."""
    return tmp_path / "config.json"


class TestGetConfig:
    """Tests for get_config."""

    def test_returns_defaults_when_no_file(self, tmp_config_path: Path) -> None:
        config = get_config(config_path=tmp_config_path)
        assert config == DEFAULT_CONFIG

    def test_creates_config_file_on_first_read(self, tmp_config_path: Path) -> None:
        get_config(config_path=tmp_config_path)
        assert tmp_config_path.exists()
        data = json.loads(tmp_config_path.read_text())
        assert data == DEFAULT_CONFIG

    def test_reads_existing_config(self, tmp_config_path: Path) -> None:
        custom = {"default_project": "myproject"}
        tmp_config_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_config_path.write_text(json.dumps(custom))
        config = get_config(config_path=tmp_config_path)
        assert config["default_project"] == "myproject"


class TestSetConfig:
    """Tests for set_config."""

    def test_set_new_value(self, tmp_config_path: Path) -> None:
        set_config("default_project", "work", config_path=tmp_config_path)
        config = get_config(config_path=tmp_config_path)
        assert config["default_project"] == "work"

    def test_set_creates_file_if_missing(self, tmp_config_path: Path) -> None:
        set_config("default_project", "work", config_path=tmp_config_path)
        assert tmp_config_path.exists()


class TestConfigShowCLI:
    """Tests for chrono config show."""

    def test_config_show_outputs_table(self, tmp_config_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["config", "show", "--config-path", str(tmp_config_path)])
        assert result.exit_code == 0
        assert "default_project" in result.output
        assert "general" in result.output


class TestConfigSetCLI:
    """Tests for chrono config set."""

    def test_config_set_updates_value(self, tmp_config_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli, ["config", "set", "default_project", "work", "--config-path", str(tmp_config_path)]
        )
        assert result.exit_code == 0
        config = get_config(config_path=tmp_config_path)
        assert config["default_project"] == "work"

    def test_config_set_confirms_update(self, tmp_config_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli, ["config", "set", "default_project", "work", "--config-path", str(tmp_config_path)]
        )
        assert result.exit_code == 0
        assert "default_project" in result.output
        assert "work" in result.output
