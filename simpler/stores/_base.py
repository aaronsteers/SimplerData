import abc
import typing as t  # noqa

from simpler.connectors import Extractor, Loader


class SQLEngine(metaclass=abc.ABCMeta):
    """Base class for SQL engines."""

    @abc.abstractmethod
    def execute(self, sql: str) -> t.Any:
        """Execute a SQL statement."""
        pass


class DatastoreBase(metaclass=abc.ABCMeta):
    """Base class for writeable data repositories or "data stores"."""

    loader: Loader
    extractor: Extractor | None
    sql_engine: SQLEngine | None
