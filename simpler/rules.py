import fnmatch
from functools import cache, cached_property


class SelectionRule:
    """A selection rule."""

    def __init__(self, /, pattern: str):
        """Initialize the selection rule."""
        self.pattern = pattern

    @cached_property
    def dataset_pattern(self) -> str:
        """Return the dataset match pattern."""
        if "." in self.pattern:
            return self.pattern.split(".")[0]
        else:
            return self.pattern

    @cached_property
    def dataset_property_pattern(self) -> str:
        """Return the dataset property match pattern."""
        if "." in self.pattern:
            return self.pattern.split(".")[:-1]
        return "*"

    @cache
    def check_dataset(self, /, name: str) -> bool:
        """Use glob rules to match pattern against the given name."""
        return fnmatch.fnmatch(name, self.pattern)

    @cache
    def check_dataset_property(self, /, name: str) -> bool:
        """Use glob rules to match pattern against the given name."""
        return fnmatch.fnmatch(name, self.pattern)
