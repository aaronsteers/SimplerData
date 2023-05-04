from simpler import naming, stack
from simpler.interop import duckdb

from . import reverse_el
from .sources import github, jaffle_shop

WAREHOUSE_DB_PATH = "./db.duckdb"


class GitHubStack(stack.DataStack):
    """My GitHub data stack."""

    name = "AJ's Data Stack"
    naming_convention = naming.SnakeCase()

    # Data sources:
    sources = [
        github.GitHubSource(),
        jaffle_shop.JaffleShopSource(),
    ]

    # 3 Stages of the DW: "raw", "internal", and "output"
    storage_scheme = duckdb.DuckDBDWStorageScheme(path=WAREHOUSE_DB_PATH)

    # Reverse EL flows that should run after the DW is ready.
    output_flows = [
        reverse_el.github_push,
        reverse_el.slack_push,
    ]
