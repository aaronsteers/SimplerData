import abc
import typing as t
from functools import cached_property

from simpler.entities import DataEntity
from simpler.naming import NamingConvention
from simpler.tables import SourceTable
from simpler.transforms._aggregate import AnalysisCalc
from simpler.transforms.sql import SQLStageTransform, SQLTransformBase


class DataStack(metaclass=abc.ABCMeta):
    """An automated data stack and data warehouse."""

    name: str
    naming_convention: NamingConvention
    sql_staging_transforms: t.Iterable[SQLTransformBase]
    sql_transforms: t.Iterable[SQLTransformBase]

    @cached_property
    def source_tables(self) -> t.Iterable[SourceTable]:
        """Tables to ingest from sources."""
        for source in self.sources:
            for table in source.tables:
                yield table

    @cached_property
    def entities(self) -> dict[str, DataEntity]:
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
    def sql_staging_transforms(self) -> t.Iterable[SQLTransformBase]:
        """SQL staging transforms for this data stack."""
        for source_table in self.source_tables:
            yield SQLStageTransform(
                source_table,
                naming_convention=self.naming_convention,
            )

    @cached_property
    def sql_transforms(self) -> t.Iterable[SQLTransformBase]:
        """SQL transforms for this data stack."""
        for _, entity in self.entities.items():
            yield from entity.sql_transforms
