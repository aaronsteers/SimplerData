import abc
import typing as t

from simpler.connectors import Source
from simpler.properties import DataProperty


class Table(metaclass=abc.ABCMeta):
    """A table."""

    name: str
    properties: t.Iterable[DataProperty]


class SourceTable(Table):
    """A source table."""

    source: Source
