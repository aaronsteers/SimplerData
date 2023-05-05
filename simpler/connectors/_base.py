import abc
import typing as t

from pydantic import BaseModel

from simpler.rules import SelectionRule


class Connector(BaseModel, metaclass=abc.ABCMeta):
    """Base class for connectors."""

    name: str

    @abc.abstractmethod
    def ensure_installed(self):
        """Ensure that the connector is installed."""
        raise NotImplementedError


class Extractor(BaseModel, metaclass=abc.ABCMeta):
    """Base class for extractors."""


class Loader(BaseModel, metaclass=abc.ABCMeta):
    """Base class for loaders."""


class Source(BaseModel, metaclass=abc.ABCMeta):
    """A source."""

    class Config:
        arbitrary_types_allowed = True

    name: str
    loader: Loader
    discover_datasets: bool
    extractor: Extractor
    ingest_rules: t.Iterable[SelectionRule]


class ConnectorConfig(BaseModel):
    """Connector config."""

    config: dict
