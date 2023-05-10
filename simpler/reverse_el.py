
from simpler.connectors import Loader
from simpler.flows import ELDataFlow
from simpler.rules import SelectionRule
from simpler.stack import DataStack
from simpler.transforms.inline import InlineTransform


class ReverseELFlow(ELDataFlow):
    """A reverse EL data flow."""

    def __init__(
        self,
        source_stack: DataStack,
        loader: Loader | None,
        rules: list[SelectionRule] | None = None,
        transforms: list[InlineTransform] | None = None,
    ):
        self.extractor = source_stack.as_extractor()
        self.loader = loader
        self.rules = rules or []
        self.transforms = transforms or []
