from functools import cached_property
from typing import t  # noqa

from simpler.connectors.singer import SingerConfig, SingerTarget
from simpler.stores import DatastoreBase


class DuckDBSingerConfig(SingerConfig):
    """DuckDB config."""


class DuckDBSingerTarget(SingerTarget):
    """DuckDB loader."""

    config: DuckDBSingerConfig


class DuckDBDatastore(DatastoreBase):
    """DuckDB datastore."""

    def __init__(self, db_name: str | None, schema_name: str | None, path: str | None):
        """Initialize the DuckDB datastore."""
        super().__init__()
        self.db_name = db_name
        self.schema_name = schema_name
        self.path = path

    @cached_property()
    def loader(self) -> DuckDBSingerTarget:
        return DuckDBSingerTarget(self.path)


class DuckDBDatabase(DuckDBDatastore):
    """DuckDB database."""

    def __init__(self, db_name: str | None, path: str | None):
        """Initialize the DuckDB database."""
        super().__init__()
        self.path = path

    @cached_property()
    def loader(self) -> SingerLoader:
        """Get a loader for this database."""
        return SingerLoader(self.path)

    def get_schema(self, schema_name: str) -> DuckDBDatastore:
        """Get a schema in this database by name."""
        return DuckDBDatastore(self.name, schema_name, self.path)
