from simpler import (
    CustomInlineTransform,
    MD5Transform,
    SelectionRule,
)
from simpler.interop.github import GitHubSingerTap, GitHubTapConfig


class GitHubSource(GitHubSingerTap):
    name = "GitHub Tap"
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
