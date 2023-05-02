from simpler.connectors.singer import SingerConfig, SingerTap


class GitHubTapConfig(SingerConfig):
    """GitHub tap config."""


class GitHubSingerTap(SingerTap):
    """GitHub tap."""

    tap_name = "tap-github"
    config: GitHubTapConfig
