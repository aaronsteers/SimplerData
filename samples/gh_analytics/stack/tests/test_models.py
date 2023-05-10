import pickle

import pytest

from simpler import ELDataFlow
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


# Create a pytest fixture for the ELDataFlow class:
@pytest.fixture
def el_data_flow():
    return ELDataFlow(
        extractor=None,
        loader=None,
    )


# Create a parameterized test for the ELDataFlow class:
@pytest.mark.parametrize(
    "model_object",
    [
        (github_push),
        (slack_push),
    ],
)
def test_model_json_out(model_object):
    _ = model_object.json()


# Create a parameterized test for the ELDataFlow class:
@pytest.mark.parametrize(
    "model_object",
    [
        (github_push),
        (slack_push),
    ],
)
def test_model_pickling(model_object):
    pickled = pickle.dumps(model_object)
    unpickled = pickle.loads(pickled)
    assert model_object.json() == unpickled.json()
