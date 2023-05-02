from typing import t

from simpler.connectors import Extractor, Loader
from simpler.rules import SelectionRule
from simpler.transforms.inline import InlineTransform


class ELDataFlow:
    extractor: Extractor
    loader: Loader
    rules: t.Iterable[SelectionRule]
    transforms: t.Iterable[InlineTransform]

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
