"""Meltano interop."""

import typing as t
from pathlib import Path

from pydantic import BaseModel
from runnow import run

from simpler import yaml
from simpler.builders import StackBuilder
from simpler.connectors.singer import SingerTap, SingerTarget
from simpler.tools import PythonExecutable, Tool, ToolType


class MeltanoCommand(BaseModel):
    """A Meltano command."""

    name: str
    executable: str | None
    args: str | None


class MeltanoUtility(BaseModel):
    """A Meltano utility."""

    name: str
    executable: PythonExecutable
    commands: list[MeltanoCommand]


class MeltanoProject(BaseModel):
    """A Meltano project."""

    project_dir: Path
    extractors: t.List[SingerTap]
    loaders: t.List[SingerTarget]
    utilities: t.List[MeltanoUtility]

    def _init_meltano(self, path: Path) -> None:
        """Initialize a Meltano project."""
        path.exists() or path.mkdir(parents=True)
        run(
            cmd="meltano init",
            working_dir=path,
        )

    def _add_plugin(
        self,
        plugin: PythonExecutable,
        type: ToolType,
        path: str,
    ) -> None:
        """Add a plugin to a Meltano project."""
        run(
            cmd=f"meltano add {type} {plugin.name}",
            working_dir=path,
        )

    def _add_extractors(self, path: str) -> None:
        """Add extractors to a Meltano project."""
        for source in self.extractors:
            source.add_to_meltano(path=path)

    def _add_loaders(self, path: str) -> None:
        """Add loaders to a Meltano project."""
        pass

    def _add_utilities(self, path: str) -> None:
        """Add utilities to a Meltano project."""
        pass

    def read_yaml(self) -> dict:
        """Read a Meltano YAML file."""
        return yaml.read_yaml(self.project_dir / "meltano.yml")


class MeltanoBuilder(StackBuilder):
    """Meltano builder."""

    project_dir: Path = Path("./.meltano")

    meltano_exe = PythonExecutable(
        executable="meltano",
        pip_urls=["meltano"],
    )

    def add_meltano_plugin(self, plugin: Tool) -> None:
        """Add a Meltano plugin."""
        self.meltano_exe.run(
            args=[
                "add",
                plugin.type,
                plugin.name,
            ],
            working_dir=self.project_dir,
        )

    def compile(
        self,
    ) -> MeltanoProject:
        """Build a Meltano project."""
        project = MeltanoProject(
            project_dir=self.project_dir,
            extractors=[],
            loaders=[],
            utilities=[],
        )
        exe = self.meltano_exe
        print(f"Creating Meltano project at '{project.project_dir.absolute()}'...")
        project.project_dir.mkdir(parents=True, exist_ok=True)
        exe.run(
            working_dir=project.project_dir,
            args="init . --force",
        )
        extractors = [source.extractor for source in self.stack.sources]
        loaders = [self.stack.as_raw_loader()]
        for plugin in extractors + loaders:
            self.add_meltano_plugin(plugin)
        return project
