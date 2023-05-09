from pydantic import Extra

from simpler.connectors._base import Extractor, Loader
from simpler.tools import ToolConfig


class SingerConfig(ToolConfig):
    """A Singer config."""


class CustomSingerConfig(SingerConfig):
    """A JSON Schema config."""

    class Config:
        extra = Extra.allow


class SingerTap(Extractor):
    """A Singer tap (extractor)."""


class SingerTarget(Loader):
    """A Singer target (loader)."""
