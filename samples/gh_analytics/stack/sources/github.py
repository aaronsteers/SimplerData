from simpler import (
    SelectionRule,
)
from simpler.connectors import Source
from simpler.interop.github import GitHubSingerTap, GitHubTapConfig


class GitHubSource(Source):
    name = "GitHub Tap"
    discover_datasets = True
    ingest_rules: list[SelectionRule] = [
        SelectionRule(pattern="*.*"),
        # CustomInlineTransform(
        #     selection=SelectionRule("*.*email*"),
        #     fn=MD5Transform,
        # ),
    ]
    config = GitHubTapConfig(
        # TODO: Add GitHub tap config
    )
    extractor = GitHubSingerTap()
