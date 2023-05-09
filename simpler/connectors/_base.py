import abc
import typing as t

from pydantic import BaseModel

from simpler.entities import DataEntity
from simpler.rules import SelectionRule
from simpler.tools import Tool, ToolType


class Connector(Tool, metaclass=abc.ABCMeta):
    """Base class for connectors."""


class Extractor(Connector, metaclass=abc.ABCMeta):
    """Base class for extractors."""

    type = ToolType.EXTRACTOR


class Loader(Connector, metaclass=abc.ABCMeta):
    """Base class for loaders."""

    type = ToolType.LOADER
    extractor: Extractor | None = None


class Source(BaseModel, metaclass=abc.ABCMeta):
    """A source."""

    class Config:
        arbitrary_types_allowed = True

    name: str
    discover_datasets: bool = True
    ingest_rules: list[SelectionRule]
    entities: t.Iterable[DataEntity] = []
    extractor: Extractor | None = None
