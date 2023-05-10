import abc
import hashlib
import typing as t

from pydantic import BaseModel

from simpler.properties import Value
from simpler.rules import SelectionRule


class InlineTransform(BaseModel, metaclass=abc.ABCMeta):
    """A transform that can be applied inline."""

    @abc.abstractmethod
    def transform(self, value: Value) -> str:
        """Transform a value."""
        ...


class MD5Transform(InlineTransform):
    """An MD5 transform."""

    def transform(self, value: Value) -> str:
        """Transform a value."""
        return hashlib.md5(value.encode("utf-8")).hexdigest()


class CustomInlineTransform(InlineTransform):
    """A custom transform that can be applied inline."""

    selection: SelectionRule
    fn: t.Callable[[Value], Value]

    def transform(self, value: Value) -> str:
        """Transform a value."""
        return self.fn(value)
