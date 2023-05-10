import typing as t

from pydantic import BaseModel


class DataProperty(BaseModel):
    """A data property."""

    name: str
    json_schema: dict
    breadcrumb: tuple[str, ...]


class Value(BaseModel):
    value: t.Any
    property: DataProperty

    class Config:
        allow_arbitrary_types = True
