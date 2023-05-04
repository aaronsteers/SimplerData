from pydantic import BaseModel, Extra, validator

from simpler.connectors._base import ConnectorConfig, Extractor, Loader


class SingerConfig(BaseModel):
    """A Singer config."""

    class Config:
        extra = Extra.allow


class CustomSingerConfig(ConnectorConfig):
    """A JSON Schema config."""

    config: dict

    def __init__(self, config: dict):
        self.config = config


class SingerConnector:
    """A Singer connector definition."""

    def __init__(
        self,
        config: SingerConfig | list[SingerConfig] | None = None,
        name: str | None = None,
        pip_url: str | None = None,
    ):
        """Initialize the connector."""
        self.name = name
        self.pip_url = pip_url
        if not config:
            self.config = CustomSingerConfig({})
            return

        if isinstance(config, SingerConfig):
            self.config = config
            return

        if isinstance(config, list):
            self.config = config[0]
            self.config.merge(config[1:])

        raise ValueError("Config was not SingerConfig or list[SingerConfig].")


class SingerTap(Extractor, SingerConnector):
    """A Singer tap (extractor)."""


class SingerTarget(Loader, SingerConnector):
    """A Singer target (loader)."""
