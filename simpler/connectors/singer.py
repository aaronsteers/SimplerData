from enum import Enum, auto
from venv import EnvBuilder

from pydantic import BaseModel, Extra
from shiv import cli as shiv_cli  # noqa: F401  # TODO: Debug shiv issues

from simpler.connectors._base import ConnectorConfig, Extractor, Loader


class SingerConfig(BaseModel):
    """A Singer config."""

    class Config:
        extra = Extra.allow


class CustomSingerConfig(ConnectorConfig):
    """A JSON Schema config."""

    config: dict


class PythonInstallMethod(Enum):
    """A Python install method."""

    AUTO = auto()
    PYZ = "pyz"
    VENV = "venv"


class PythonExecutable(BaseModel):
    """A Python executable."""

    # Pip URL resources, with the first items considered primary/default:
    pip_urls: list[str]

    # Allows for custom constraints without overriding pip urls:
    pip_constraints: list[str] | None = None

    # If blank, use library name from first item in self.pip_urls:
    executable: str | None

    # Allow overriding the interpreter path:
    interpreter: str | None = None

    # Only one of these should be set:
    venv_path: str | None
    pyz_path: str | None

    @property
    def venv_path(self) -> str:
        """Return the path to the virtual environment."""
        return f"venv/{self.pip_urls[0]}"

    @property
    def pyz_path(self) -> str:
        """Return the path to the virtual environment."""
        return f"pyz/{self.pip_urls[0]}"

    @property
    def is_installed(self) -> bool:
        """Return whether the executable is installed."""
        return False

    def install(
        self,
        skip_if_installed: bool = True,
        install_method: PythonInstallMethod = PythonInstallMethod.AUTO,
    ) -> None:
        """Install the executable."""
        if self.is_installed and skip_if_installed:
            return

        if install_method == PythonInstallMethod.AUTO:
            install_method = PythonInstallMethod.VENV

        print(
            f"Installing '{self.executable}' "
            f"(pip install {' '.join(self.pip_urls)})..."
        )
        if install_method == PythonInstallMethod.PYZ:
            self._install_pyz()

        if install_method == PythonInstallMethod.VENV:
            self._install_venv()
        print(f"Completed installing '{self.executable}'.")

    def _install_pyz(self) -> None:
        """Install the pyz executable using shiv."""
        # TODO: Implement Shiv installation.
        # shiv_cli.main(
        #     self.pip_urls,
        #     console_script=self.executable,
        #     target=self.pyz_path,
        #     interpreter=self.interpreter,
        #     compressed=True,
        # )
        raise NotImplementedError("Pyz installation is not yet supported.")

    def _install_venv(self) -> None:
        """Install the executable using a virtual environment."""
        if self.interpreter:
            raise NotImplementedError(
                f"Cannot install {self.executable} with custom '{self.interpreter}' "
                "python interpreter. Customer interpreters are not yet supported."
            )
        builder = EnvBuilder(system_site_packages=False, with_pip=True)
        builder.create(self.venv_path)

    def ensure_installed(self) -> None:
        """Ensure that the executable is installed."""
        if not self.is_installed:
            print(f"Connector {self.executable} is not installed. ")
            self.install()


class SingerConnector(BaseModel):
    """A Singer connector definition."""

    name: str | None
    executable: PythonExecutable | None
    config: SingerConfig | None

    # def __init__(
    #     self,
    #     config: SingerConfig | None = None,
    #     name: str | None = None,
    #     executable: PythonExecutable | None = None,
    # ):
    #     """Initialize the connector."""
    #     self.name = name
    #     self.executable = executable
    #     if not config:
    #         self.config = CustomSingerConfig({})
    #         return

    #     if isinstance(config, SingerConfig):
    #         self.config = config
    #         return

    #     if isinstance(config, list):
    #         self.config = config[0]
    #         self.config.merge(config[1:])

    #     raise ValueError("Config was not SingerConfig or list[SingerConfig].")


class SingerTap(SingerConnector, Extractor):
    """A Singer tap (extractor)."""


class SingerTarget(SingerConnector, Loader):
    """A Singer target (loader)."""
