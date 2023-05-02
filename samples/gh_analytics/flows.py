"""My publish workflows."""


from simpler.flows import ELDataFlow
from simpler.rules import SelectionRule
from simpler.connectors.singer import SingerTarget

class GitHubFlowTarget(SingerTarget):
    ...

class SlackFlowTarget(SingerTarget):
    ...

class GitHubReverseETL(ELDataFlow):
    """My publish workflow."""

    name = "AJ's GitHub Push"
    rules = [
        # Use the full `flowto_github_notifications` table as source data.
        SelectionRule("flowto_github_notifications.*")
    ]
    loader = GitHubFlowTarget()


class SlackReverseETL(ELDataFlow):
    """My publish workflow."""

    name = "AJ's Slack Push"
    rules = [
        # Use the full `flowto_slack_notifications` table as source data.
        SelectionRule("flowto_slack_notifications.*")
    ]
    loader = SlackFlowTarget()
