import abc

from simpler.properties import DataProperty


class DataEntity(metaclass=abc.ABCMeta):
    """A data entity."""

    name: str
    properties: list[DataProperty]

    def merge(self, /, other: "DataEntity") -> None:
        """Merge this entity with another."""
        for property in other.properties:
            if property.name in self.properties:
                self.properties[property.name].merge(property)
            else:
                self.properties[property.name] = property
