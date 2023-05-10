import abc

from pydantic import BaseModel

from simpler.connectors._base import Source
from simpler.properties import DataProperty


class Table(BaseModel, metaclass=abc.ABCMeta):
    """A table."""

    name: str
    properties: list[DataProperty]


class SourceTable(Table):
    """A source table."""

    source: Source
