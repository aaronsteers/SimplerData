from simpler import (
    SelectionRule,
)
from simpler.connectors.singer import SingerConfig, SingerTap


class JaffleShopTapConfig(SingerConfig):
    """Jaffle Shop tap config."""


class JaffleShopSource(SingerTap):
    """Jaffle Shop data source."""

    name = "Jaffle Shop"
    discover_datasets = True
    extractor = SingerTap(
        name="tap-jaffle-shop",
        pip_url="tap-jaffle-shop",
        config=SingerConfig(years=1),
    )
    ingest_rules = [
        SelectionRule("*.*"),
    ]
    config = JaffleShopTapConfig(
        # TODO: Add Jaffle Shop tap config
    )
