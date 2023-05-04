"""My publish workflows."""


from simpler.connectors.singer import CustomSingerConfig, SingerTarget
from simpler.flows import ReverseELFlow
from simpler.rules import SelectionRule


class GitHubReverseEL(ReverseELFlow):
    """My publish workflow."""

    name = "AJ's GitHub Push"
    rules = [
        # Use the full `flowto_github_notifications` table as source data.
        SelectionRule("flowto_github_notifications.*")
    ]
    loader = SingerTarget(
        name="target-github",
        pip_url="target-github",
        config=CustomSingerConfig({}),
    )


class SlackReverseEL(ReverseELFlow):
    """My publish workflow."""

    name = "AJ's Slack Push"
    rules = [
        # Use the full `flowto_slack_notifications` table as source data.
        SelectionRule("flowto_slack_notifications.*")
    ]
    loader = SingerTarget(
        name="target-apprise",
        pip_url="target-apprise",
        config=CustomSingerConfig({}),
    )
