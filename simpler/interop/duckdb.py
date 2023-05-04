import typing as t  # noqa

from simpler.connectors.singer import SingerConfig, SingerTarget
from simpler.stores import DatastoreBase, DWStorageScheme
from pydantic import validator


class DuckDBSingerConfig(SingerConfig):
    """DuckDB config."""


class DuckDBSingerTarget(SingerTarget):
    """DuckDB loader."""

    name = "target-duckdb"
    config: DuckDBSingerConfig


class DuckDBDatastore(DatastoreBase):
    """DuckDB datastore."""

    db_name: str
    schema_name: t.Optional[str]
    path: str

    def __init__(self, *args, **kwargs):
        kwargs["loader"] = DuckDBSingerTarget(
            config=DuckDBSingerConfig(path=kwargs["path"])
        )
        super().__init__(**kwargs)


class DuckDBDatabase(DuckDBDatastore):
    """DuckDB database."""

    def __init__(self, db_name: str | None, path: str | None):
        """Initialize the DuckDB database."""
        super().__init__()
        self.path = path

    # @cached_property
    def loader(self) -> SingerTarget:
        """Get a loader for this database."""
        return SingerTarget(self.path)

    def get_schema(self, schema_name: str) -> DuckDBDatastore:
        """Get a schema in this database by name."""
        return DuckDBDatastore(self.name, schema_name, self.path)

    @staticmethod
    def db_name_from_path(path: str) -> str:
        """Get a database name from a path."""
        return path.split("/")[-1].split(".")[0]


class DuckDBDWStorageScheme(DWStorageScheme):
    """A storage scheme for a DuckDB data warehouse."""

    path: str
    raw: DuckDBDatastore
    internal: DuckDBDatastore
    output: DuckDBDatastore

    def __init__(
        self,
        path: str,
        raw_schema_name="raw",
        internal_schema_name="internal",
        output_schema_name="output",
    ):
        """Initialize the DuckDB data warehouse storage scheme."""
        db_name = DuckDBDatabase.db_name_from_path(path)
        super().__init__(
            path=path,
            raw=DuckDBDatastore(
                db_name=db_name, scheme_name=raw_schema_name, path=path
            ),
            internal=DuckDBDatastore(
                db_name=db_name, scheme_name=internal_schema_name, path=path
            ),
            output=DuckDBDatastore(
                db_name=db_name, scheme_name=output_schema_name, path=path
            ),
        )


__all__ = [
    "DuckDBSingerConfig",
    "DuckDBSingerTarget",
    "DuckDBDatastore",
    "DuckDBDatabase",
    "DuckDBDWStorageScheme",
]
