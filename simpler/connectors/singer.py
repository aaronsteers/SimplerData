from simpler.connectors._base import Extractor, Loader


class SingerConfig(dict):
    """A Singer config."""


class SingerConnector:
    """A Singer connector definition."""

    config: SingerConfig


class SingerTap(Extractor, metaclass=SingerConnector):
    """A Singer tap (extractor)."""

    tap_name: str

    def name(self) -> str:
        """Return the name of this extractor."""
        return self.tap_name.replace("tap-", "")


class SingerTarget(Loader, metaclass=SingerConnector):
    """A Singer target (loader)."""

    target_name: str

    def name(self) -> str:
        """Return the name of this loader."""
        return self.target_name.replace("target-", "")
