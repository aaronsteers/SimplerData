import typing as t

from simpler.flows import ELDataFlow
from simpler.interop.duckdb import DuckDBDatastore
from simpler.stack import DataStack

from ...simpler.naming import SnakeCase
from .sources import (
    GitHubSource,
    JaffleShopSource,
)

WAREHOUSE_DB_PATH = "./db.duckdb"


class MyDW(DataStack):
    """My data stack."""

    name = "AJ's Data Stack"
    naming_convention = SnakeCase()

    # Data sources:
    sources = [GitHubSource(), JaffleShopSource()]

    # 3 Stages of the DW: "raw", "internal", and "output"
    raw_datastore = DuckDBDatastore("DuckDB", "raw")
    internal_datastore = DuckDBDatastore("DuckDB", "internal")
    output_datastore = DuckDBDatastore("DuckDB", "marts")

    # Reverse ETL flows that should run after the DW is ready.
    publish_flows = t.Iterable[ELDataFlow]


def main():
    dw = MyDW()
    dw.compile()
    dw.build()
    dw.publish()


if __name__ == "__main__":
    main()
