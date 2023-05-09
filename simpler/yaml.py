"""Wrapper around yaml libraries."""

from pathlib import Path

from ruamel.yaml import YAML


def read_yaml(stream: Path, /) -> dict:
    """Load a YAML file."""
    yaml = YAML()
    yaml.default_flow_style = False
    return yaml.load(stream)


def write_yaml(data: dict, /, path: Path) -> dict:
    """Load a YAML file."""
    yaml = YAML()
    yaml.default_flow_style = False
    return yaml.dump(data, stream=path)
