from pathlib import Path

from samples.gh_analytics.stack.stack import GitHubStackBuilder


def test_stack():
    builder = GitHubStackBuilder()
    builder.compile()


def test_manifest():
    builder = GitHubStackBuilder()
    builder.write_manifest(Path("./manifest.json"))
