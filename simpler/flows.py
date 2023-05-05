import abc
import typing as t

from pydantic import BaseModel

from simpler.connectors import Extractor, Loader
from simpler.rules import SelectionRule
from simpler.transforms.inline import InlineTransform


class ELDataFlow(BaseModel, metaclass=abc.ABCMeta):
    extractor: Extractor | None
    loader: Loader | None
    rules: t.Iterable[SelectionRule] = []
    transforms: t.Iterable[InlineTransform] = []

    class Config:
        arbitrary_types_allowed = True

    def ensure_installed(self):
        for connector in (self.extractor, self.loader):
            if connector.executable is None:
                raise ValueError(
                    f"Connector executable for '{connector.name}' is None."
                )
            # if connector is not None and connector.executable is not None:
            connector.executable.ensure_installed()

    def run(self, **kwargs) -> None:
        """Run the data flow."""
        self.ensure_installed()
        print(
            f"Emulating sync from extractor '{self.extractor.name}' "
            f"to '{self.loader.name}'."
        )
        # raise NotImplementedError


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
        **kwargs,
    ):
        super().__init__(
            extractor=None,
            **kwargs,
        )
