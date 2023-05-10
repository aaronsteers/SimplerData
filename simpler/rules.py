import fnmatch
from functools import cached_property

from pydantic import BaseModel


class SelectionRule(BaseModel):
    """A selection rule."""

    pattern: str

    class Config:
        arbitrary_types_allowed = True

    @cached_property
    def _dataset_pattern(self) -> str:
        """Return the dataset match pattern."""
        if "." in self.pattern:
            return self.pattern.split(".")[0]
        else:
            return self.pattern

    @cached_property
    def _dataset_property_pattern(self) -> str:
        """Return the dataset property match pattern."""
        if "." in self.pattern:
            return self.pattern.split(".")[:-1]
        return "*"

    def check_dataset(self, /, name: str) -> bool:
        """Use glob rules to match pattern against the given name."""
        return fnmatch.fnmatch(name, self.pattern)

    def check_dataset_property(self, /, name: str) -> bool:
        """Use glob rules to match pattern against the given name."""
        return fnmatch.fnmatch(name, self.pattern)
