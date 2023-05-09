import abc
from enum import Enum, auto
from pathlib import Path
from venv import EnvBuilder

from pydantic import BaseModel
from runnow import run


class ToolType(Enum):
    """Tool type."""

    EXTRACTOR = "extractor"
    LOADER = "loader"
    UTILITY = "utility"


class ExecutableBase(BaseModel, metaclass=abc.ABCMeta):
    """Base class for executables."""

    executable: str

    @property
    def is_installed(self) -> bool:
        """Return whether the executable is installed."""
        raise NotImplementedError()

    @abc.abstractmethod
    def install(
        self,
        skip_if_installed: bool = True,
        **kwargs,
    ) -> None:
        """Install the executable."""
        ...

    def ensure_installed(self) -> None:
        """Ensure that the executable is installed."""
        if not self.is_installed:
            print(f"'{self.executable}' is not installed. ")
            self.install()

    def run(
        self,
        args: str | list[str],
        working_dir: str | Path,
    ) -> None:
        """Execute the executable."""
        if isinstance(args, str):
            args = args.split(" ")

        run(
            " ".join([self.executable, *args]),
            working_dir=working_dir,
        )


class PreinstalledExecutable(ExecutableBase):
    """A preinstalled executable."""

    @property
    def is_installed(self) -> bool:
        """Return whether the executable is installed."""
        return True

    def install(
        self,
        skip_if_installed: bool = True,
        **kwargs,
    ) -> None:
        """Install the executable."""
        _ = skip_if_installed, kwargs
        print(f"Skipping installation of '{self.executable}'. (Already installed.)")


class PythonInstallMethod(Enum):
    """A Python install method."""

    AUTO = auto()
    PYZ = "pyz"
    VENV = "venv"


class PythonExecutable(ExecutableBase):
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


class ToolConfig(BaseModel):
    """Tool config."""


class Tool(BaseModel):
    """Base class for tools."""

    name: str
    executable: ExecutableBase
    type: ToolType
    home_dir: str | Path | None = None
    config: ToolConfig | None = None

    def ensure_installed(self):
        """Ensure that the connector is installed."""
        if self.executable is not None:
            self.executable.ensure_installed()

    def run(
        self,
        args: str | list[str],
        working_dir: str | Path,
    ) -> None:
        """Execute the executable."""
        self.executable.run(
            [self.executable, *args],
            cwd=working_dir,
        )
