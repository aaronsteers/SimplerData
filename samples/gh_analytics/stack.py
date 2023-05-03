import typing as t

from simpler.flows import ELDataFlow
from simpler.interop.duckdb import DuckDBDatastore
from simpler.naming import SnakeCase
from simpler.stack import DataStack

from .sources.github import GitHubSource
from .sources.jaffle_shop import JaffleShopSource

WAREHOUSE_DB_PATH = "./db.duckdb"


class GitHubStack(DataStack):
    """My GitHub data stack."""

    name = "AJ's Data Stack"
    naming_convention = SnakeCase()

    # Data sources:
    sources = [GitHubSource(), JaffleShopSource()]

    # 3 Stages of the DW: "raw", "internal", and "output"
    raw_datastore = DuckDBDatastore("DuckDB", "raw", WAREHOUSE_DB_PATH)
    internal_datastore = DuckDBDatastore("DuckDB", "internal", WAREHOUSE_DB_PATH)
    output_datastore = DuckDBDatastore("DuckDB", "marts", WAREHOUSE_DB_PATH)

    # Reverse ETL flows that should run after the DW is ready.
    publish_flows = t.Iterable[ELDataFlow]


def main():
    dw = GitHubStack()
    dw.compile()
    dw.build()
    dw.publish()


if __name__ == "__main__":
    main()
