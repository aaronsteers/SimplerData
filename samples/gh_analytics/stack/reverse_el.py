"""My publish workflows."""


from simpler.connectors.singer import CustomSingerConfig, SingerTarget
from simpler.flows import ReverseELFlow
from simpler.rules import SelectionRule
from simpler.tools import PythonExecutable

github_push = ReverseELFlow(
    name="AJ's GitHub Push",
    rules=[
        # Use the full `flowto_github_notifications` table as source data.
        SelectionRule(pattern="flowto_github_notifications.*")
    ],
    loader=SingerTarget(
        name="target-github",
        config=CustomSingerConfig(),
        executable=PythonExecutable(
            pip_urls=["target-github"],
            executable="target-github",
        ),
    ),
)

slack_push = ReverseELFlow(
    name="AJ's Slack Push",
    rules=[
        # Use the full `flowto_slack_notifications` table as source data.
        SelectionRule(pattern="flowto_slack_notifications.*")
    ],
    loader=SingerTarget(
        name="target-apprise",
        config=CustomSingerConfig(),
        executable=PythonExecutable(
            pip_urls=["target-apprise"],
            executable="target-apprise",
        ),
    ),
)
