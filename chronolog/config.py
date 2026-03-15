"""Configuration system for ChronoLog."""

import json
from pathlib import Path


DEFAULT_CONFIG: dict[str, str] = {
    "default_project": "general",
}


def _default_config_path() -> Path:
    """Return the default config file path.

    Returns:
        Path to ~/.chronolog/config.json.
    """
    return Path.home() / ".chronolog" / "config.json"


def get_config(config_path: Path | None = None) -> dict[str, str]:
    """Read the configuration file, creating it with defaults if missing.

    Args:
        config_path: Path to config file. Defaults to ~/.chronolog/config.json.

    Returns:
        A dict of configuration key-value pairs.
    """
    if config_path is None:
        config_path = _default_config_path()

    if config_path.exists():
        return json.loads(config_path.read_text())

    # Create with defaults
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
    return dict(DEFAULT_CONFIG)


def set_config(key: str, value: str, config_path: Path | None = None) -> None:
    """Set a configuration value and write to file.

    Args:
        key: The config key to set.
        value: The value to assign.
        config_path: Path to config file. Defaults to ~/.chronolog/config.json.
    """
    if config_path is None:
        config_path = _default_config_path()

    config = get_config(config_path=config_path)
    config[key] = value
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))
