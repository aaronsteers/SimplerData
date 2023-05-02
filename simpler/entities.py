import abc
import typing as t
from functools import cached_property

from simpler.properties import DataProperty
from simpler.transforms.sql import SQLTransformBase


class DataEntity(metaclass=abc.ABCMeta):
    """A data entity."""

    name: str
    properties: t.Iterable[DataProperty]

    @cached_property
    def sql_transforms(self) -> t.Iterable[SQLTransformBase]:
        """SQL transforms for this entity."""
        for property in self.properties:
            yield from property.sql_transforms

    def merge(self, /, other: "DataEntity") -> None:
        """Merge this entity with another."""
        for property in other.properties:
            if property.name in self.properties:
                self.properties[property.name].merge(property)
            else:
                self.properties[property.name] = property
