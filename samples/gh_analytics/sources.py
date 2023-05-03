from simpler import (
    CustomInlineTransform,
    MD5Transform,
    SelectionRule,
)
from simpler.connectors.singer import SingerConfig, SingerTap
from simpler.interop.github import GitHubSingerTap, GitHubTapConfig


class GitHubSource(GitHubSingerTap):
    name = "GitHub"
    discover_datasets = True
    ingest_rules = [
        SelectionRule("*.*"),
        CustomInlineTransform(
            selection=SelectionRule("*.*email*"),
            transform=MD5Transform,
        ),
    ]
    config = GitHubTapConfig(
        # TODO: Add GitHub tap config
    )


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
