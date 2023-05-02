import abc
import typing as t

from simpler.rules import SelectionRule


class Extractor(metaclass=abc.ABCMeta):
    """Base class for extractors."""

    name: str


class Loader(metaclass=abc.ABCMeta):
    """Base class for loaders."""

    name: str


class Source(metaclass=abc.ABCMeta):
    """A source."""

    name: str
    loader: Loader
    discover_datasets: bool
    extractor: Extractor
    ingest_rules: Iterable[SelectionRule]
