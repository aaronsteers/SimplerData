from simpler.connectors.singer import SingerExtractor, SingerTap
from simpler.interop.github import GitHubSingerTap, GitHubTapConfig

from ...simpler import (
    CustomInlineTransform,
    MD5Transform,
    SelectionRule,
)


class GitHubSource(GitHubSingerTap):
    name = "GitHub"
    discover_datasets = True
    ingest_rules = [
        SelectionRule("*.*"),
        CustomInlineTransform(
            condition=lambda x: x.property.name.contains("email"),
            transform=MD5Transform,
        ),
    ]
    config = GitHubTapConfig(
        # TODO: Add GitHub tap config
    )


class JaffleShopSource(SingerTap):
    """Jaffle Shop data source."""

    name = "Jaffle Shop"
    discover_datasets = True
    extractor = SingerExtractor(
        tap="tap-jaffle-shop",
        config={"years": 1},
    )
    ingest_rules = [
        SelectionRule("*.*"),
    ]
    config = JaffleShopTapConfig(
        # TODO: Add Jaffle Shop tap config
    )
