import typing as t


class DataProperty:
    """A data property."""

    name: str
    json_schema: dict
    breadcrumb: tuple[str, ...]


class Value:
    value: t.Any
    property: DataProperty
