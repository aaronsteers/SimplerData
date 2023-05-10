from simpler import ELDataFlow, Source, naming, stack
from simpler.interop import duckdb, meltano

from . import reverse_el
from .sources import github, jaffle_shop

WAREHOUSE_DB_PATH = "./db.duckdb"


class GitHubStack(stack.DataStack):
    """My GitHub data stack."""

    name = "AJ's Data Stack"
    storage_scheme = duckdb.DuckDBDWStorageScheme(path=WAREHOUSE_DB_PATH)
    naming_convention = naming.SnakeCase()
    sources: list[Source] = [
        github.GitHubSource(),
        jaffle_shop.JaffleShopSource(),
    ]
    output_flows: list[ELDataFlow] = [
        reverse_el.github_push,
        reverse_el.slack_push,
    ]
    entities = {}


class GitHubTestStack(GitHubStack):
    name = "AJ's Test Data Stack"
    storage_scheme = duckdb.DuckDBDWStorageScheme(path=WAREHOUSE_DB_PATH + ".test")
    config = [
        github.GitHubTapConfig(
            start_date="2020-01-01",
        ),
        jaffle_shop.JaffleShopTapConfig(
            years=3,
        ),
    ]


class GitHubStackBuilder(meltano.MeltanoBuilder):
    stack = GitHubStack()
