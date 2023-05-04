import abc
import typing as t

from simpler.connectors import Extractor, Loader
from simpler.rules import SelectionRule
from simpler.transforms.inline import InlineTransform


class ELDataFlow(metaclass=abc.ABCMeta):
    extractor: Extractor
    loader: Loader
    rules: t.Iterable[SelectionRule]
    transforms: t.Iterable[InlineTransform]


class CustomELFlow(ELDataFlow):
    """A custom EL data flow."""

    def __init__(
        self,
        extractor: Extractor | None,
        loader: Loader | None,
        rules: t.Iterable[SelectionRule] | None = None,
        transforms: t.Iterable[InlineTransform] | None = None,
    ):
        self.extractor = extractor
        self.loader = loader
        self.rules = rules or []
        self.transforms = transforms or []


class ReverseELFlow(ELDataFlow):
    """A reverse EL data flow, where the extractor is the data warehouse."""

    def __init__(
        self,
        loader: Loader | None = None,
        rules: t.Iterable[SelectionRule] | None = None,
        transforms: t.Iterable[InlineTransform] | None = None,
    ):
        self.extractor = None  # The DW is the extraction sources.
        self.loader = loader or self.__class__.loader
        self.rules = rules or self.__class__.rules or []
        self.transforms = transforms or []
