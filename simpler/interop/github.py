from simpler.connectors.singer import SingerConfig, SingerTap
from simpler.tools import PythonExecutable


class GitHubTapConfig(SingerConfig):
    """GitHub tap config."""


class GitHubSingerTap(SingerTap):
    """GitHub tap."""

    name = "tap-github"
    config: GitHubTapConfig = GitHubTapConfig()
    executable = PythonExecutable(
        executable="tap-github",
        pip_urls=["tap-github"],
        # interpreter=PythonInterpreter.PYTHON_3_9,
    )
