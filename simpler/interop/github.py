from simpler.connectors.singer import PythonExecutable, SingerConfig, SingerTap


class GitHubTapConfig(SingerConfig):
    """GitHub tap config."""


class GitHubSingerTap(SingerTap):
    """GitHub tap."""

    tap_name = "tap-github"
    config: GitHubTapConfig
    executable = PythonExecutable(
        executable="tap-github",
        pip_urls=["tap-github"],
        # interpreter=PythonInterpreter.PYTHON_3_9,
    )
