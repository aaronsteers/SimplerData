from simpler import (
    SelectionRule,
)
from simpler.connectors.singer import PythonExecutable, SingerConfig, SingerTap


class JaffleShopTapConfig(SingerConfig):
    """Jaffle Shop tap config."""

    years: int = 1


class JaffleShopSource(SingerTap):
    """Jaffle Shop data source."""

    name = "Jaffle Shop"
    discover_datasets = True
    executable = PythonExecutable(
        pip_urls=["tap-jaffle-shop"],
        executable="tap-jaffle-shop",
        # interpreter="python3.9",  # TODO: Add interpreter override option
    )
    ingest_rules = [
        SelectionRule("*.*"),
    ]
    config = JaffleShopTapConfig(
        years=1,
    )
