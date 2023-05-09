"""Meltano interop."""

import typing as t
from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from runnow import run

from simpler import yaml
from simpler.connectors import Extractor, Loader, Source
from simpler.connectors.singer import PythonExecutable, SingerTap, SingerTarget
from simpler.flows import ReverseELFlow
from simpler.stores import DatastoreBase, DWStorageScheme
from simpler.tools import ToolType


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


class MeltanoBuilder(BaseModel):
    """Meltano builder."""

    sources: t.List[SingerTap] = []
    storage_scheme: DWStorageScheme
    output_flows: t.List[ReverseELFlow] = []
    meltano_exe = PythonExecutable(
        executable="meltano",
        pip_urls=["meltano"],
    )

    def build(self, path: str = "./.meltano") -> MeltanoProject:
        """Build a Meltano project."""
        project = MeltanoProject(
            project_dir=Path(path),
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
        for source in self.sources:
            exe.run(
                working_dir=project.project_dir,
                args=[
                    "add",
                    "extractor",
                    source.name,
                ],
            )
        for loader in [self.storage_scheme.raw.loader]:
            exe.run(
                working_dir=project.project_dir,
                args=[
                    "add",
                    "loader",
                    loader.name,
                ],
            )
        return project
