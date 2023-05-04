"""My publish workflows."""


from simpler.connectors.singer import CustomSingerConfig, SingerTarget
from simpler.flows import ReverseELFlow
from simpler.rules import SelectionRule

github_push = ReverseELFlow(
    name="AJ's GitHub Push",
    rules=[
        # Use the full `flowto_github_notifications` table as source data.
        SelectionRule("flowto_github_notifications.*")
    ],
    loader=SingerTarget(
        name="target-github",
        pip_url="target-github",
        config=CustomSingerConfig(config={}),
    ),
)

slack_push = ReverseELFlow(
    name="AJ's Slack Push",
    rules=[
        # Use the full `flowto_slack_notifications` table as source data.
        SelectionRule("flowto_slack_notifications.*")
    ],
    loader=SingerTarget(
        name="target-apprise",
        pip_url="target-apprise",
        config=CustomSingerConfig(config={}),
    ),
)
