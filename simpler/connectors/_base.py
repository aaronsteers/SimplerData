import abc
import typing as t

from pydantic import BaseModel

from simpler.rules import SelectionRule


class Extractor(BaseModel, metaclass=abc.ABCMeta):
    """Base class for extractors."""

    name: str


class Loader(BaseModel, metaclass=abc.ABCMeta):
    """Base class for loaders."""

    name: str


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
