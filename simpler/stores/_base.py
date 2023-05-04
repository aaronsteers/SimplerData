import abc
import typing as t

from pydantic import BaseModel  # noqa

from simpler.connectors import Extractor, Loader


class SQLEngine(metaclass=abc.ABCMeta):
    """Base class for SQL engines."""

    @abc.abstractmethod
    def execute(self, sql: str) -> t.Any:
        """Execute a SQL statement."""
        pass


class DatastoreBase(BaseModel, metaclass=abc.ABCMeta):
    """Base class for writeable data repositories or "data stores"."""

    class Config:
        arbitrary_types_allowed = True

    loader: Loader
    extractor: Extractor | None
    sql_engine: SQLEngine | None


class StorageSchemeBase(BaseModel, metaclass=abc.ABCMeta):
    raw: DatastoreBase
    output: DatastoreBase


class DWStorageScheme(StorageSchemeBase):
    """A storage scheme for a data warehouse."""

    raw: DatastoreBase
    internal: DatastoreBase
    output: DatastoreBase
