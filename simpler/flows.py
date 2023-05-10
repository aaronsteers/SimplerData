
from pydantic import BaseModel

from simpler.connectors import Loader, Source
from simpler.rules import SelectionRule
from simpler.transforms.inline import InlineTransform


class ELDataFlow(BaseModel):
    source: Source | None
    loader: Loader | None
    rules: list[SelectionRule] = []
    transforms: list[InlineTransform] = []

    class Config:
        arbitrary_types_allowed = True

    def ensure_installed(self):
        for name, executable in (
            (self.source.name, self.source.extractor),
            (self.loader.name, self.loader),
        ):
            if executable is None:
                raise ValueError(f"Connector executable for '{name}' is None.")
            # if connector is not None and connector.executable is not None:
            executable.ensure_installed()

    def run(self, **kwargs) -> None:
        """Run the data flow."""
        self.ensure_installed()
        print(
            f"Emulating sync from extractor '{self.source.name}' "
            f"to '{self.loader.name}'."
        )
        # raise NotImplementedError


class ReverseELFlow(ELDataFlow):
    """A reverse EL data flow, where the extractor is the data warehouse."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            extractor=kwargs.pop("extractor", None),
            **kwargs,
        )
