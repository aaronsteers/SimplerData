from simpler import (
    SelectionRule,
)
from simpler.connectors import Source
from simpler.connectors.singer import PythonExecutable, SingerConfig, SingerTap


class JaffleShopTapConfig(SingerConfig):
    """Jaffle Shop tap config."""

    years: int = 1


class JaffleShopSource(Source):
    """Jaffle Shop data source."""

    name = "Jaffle Shop"
    discover_datasets = True
    ingest_rules: list[SelectionRule] = [
        SelectionRule("*.*"),
    ]
    config = JaffleShopTapConfig(
        years=1,
    )
    extractor = SingerTap(
        name="tap-jaffle-shop",
        executable=PythonExecutable(
            pip_urls=["tap-jaffle-shop"],
            executable="tap-jaffle-shop",
            # interpreter="python3.9",  # TODO: Add interpreter override option
        ),
        config=JaffleShopTapConfig(),
    )
