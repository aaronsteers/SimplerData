import abc


class NamingConvention(metaclass=abc.ABCMeta):
    """Naming convention base class."""

    name: str
    allow_start_with_number = False
    allow_fully_numeric = False

    @property
    def _illegal_chars(self) -> list[str]:
        return "-:;,.?!@#$%^&*()+=/\\|{}[]`~"

    @property
    def normalization_prefix() -> str:
        """Prefix to apply if needed, for instance if name begins with a number."""
        return "c_"

    def requires_prefix(self, /, name: str) -> bool:
        if name[0].isnumeric():
            if not self.allow_start_with_number:
                return True
            elif not self.allow_fully_numeric and name.isnumeric():
                return True
        return False

    def transform(self, /, name: str) -> str:
        result = name.translate({ord(i): None for i in self._illegal_chars})
        if self.requires_prefix(name):
            result = self.normalization_prefix + result
        return result

    def check(self, /, name: str) -> bool:
        return self.transform(name) == name


class PascalCase(NamingConvention):
    """Pascal case naming convention."""

    name = "pascal case"

    def transform(self, name: str) -> str:
        return super().transform(name).replace("_", " ").title().replace("_", "")


class CamelCase(PascalCase):
    """Camel case naming convention."""

    name = "camel case"

    def transform(self, name: str) -> str:
        result = super().transform(name)
        return result[0].lower() + result[1:]


class SnakeCase(NamingConvention):
    """Camel case naming convention."""

    name = "snake case"

    def transform(self, name: str) -> str:
        result = super().transform(name)
        return result.lower().replace(" ", "_")
