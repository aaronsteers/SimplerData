import abc
import typing as t
from functools import cached_property

from pydantic import BaseModel

from simpler.calculations import AnalysisCalc
from simpler.connectors import Extractor, Loader, Source
from simpler.entities import DataEntity
from simpler.flows import ELDataFlow
from simpler.interop.duckdb import DuckDBDWStorageScheme
from simpler.naming import NamingConvention, SnakeCase
from simpler.stores import StorageScheme
from simpler.tables import SourceTable
from simpler.transforms.sql import SQLStageTransform, SQLTransformBase


class DataStack(BaseModel, metaclass=abc.ABCMeta):
    """An automated data stack and data warehouse."""

    class Config:
        arbitrary_types_allowed = True

    name: str
    naming_convention: NamingConvention = SnakeCase()

    # Data sources:
    sources: list[Source]

    # Reverse EL flows that should run after the DW is ready.
    output_flows: list[ELDataFlow] = []

    sql_staging_transforms: list[SQLTransformBase] = []
    sql_transforms: list[SQLTransformBase] = []
    storage_scheme: StorageScheme = DuckDBDWStorageScheme(
        path="./.duckdb/db.duckdb",
    )

    @cached_property
    def _source_tables(self) -> t.Iterable[SourceTable]:
        """Tables to ingest from sources."""
        for source in self.sources:
            for table in source.tables:
                yield table

    @cached_property
    def _entities(self) -> dict[str, DataEntity]:
        """Entities represented in the data warehouse."""
        entities = {}
        for source in self.sources:
            for entity in source.entities:
                if entity.name in entities:
                    entities[entity.name].merge(entity)
                else:
                    entities[entity.name] = entity
        return entities

    def analyses(self) -> t.Iterable[AnalysisCalc]:
        """Analyses for this data stack."""
        for entity in self.entities:
            yield from entity.analyses

    @cached_property
    def _sql_staging_transforms(self) -> t.Iterable[SQLTransformBase]:
        """SQL staging transforms for this data stack."""
        for source_table in self.source_tables:
            yield SQLStageTransform(
                source_table,
                naming_convention=self.naming_convention,
            )

    @cached_property
    def _sql_transforms(self) -> t.Iterable[SQLTransformBase]:
        """SQL transforms for this data stack."""
        for _, entity in self.entities.items():
            yield from entity.sql_transforms

    def as_raw_loader(self) -> Loader:
        """Return this data stack as a loader for raw data."""
        return self.storage_scheme.raw.loader

    # Reverse EL

    def as_extractor(self) -> Extractor:
        """Return this data stack as an extractor."""
        return Extractor(self)
