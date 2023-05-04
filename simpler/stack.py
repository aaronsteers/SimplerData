import abc
import typing as t
from functools import cached_property

from simpler.calculations import AnalysisCalc
from simpler.connectors import Extractor, Source
from simpler.entities import DataEntity
from simpler.flows import ELDataFlow
from simpler.naming import NamingConvention
from simpler.stores import DatastoreBase
from simpler.tables import SourceTable
from simpler.transforms.sql import SQLStageTransform, SQLTransformBase


class DataStack(metaclass=abc.ABCMeta):
    """An automated data stack and data warehouse."""

    name: str
    naming_convention: NamingConvention
    sql_staging_transforms: t.Iterable[SQLTransformBase]
    sql_transforms: t.Iterable[SQLTransformBase]

    # Data sources:
    sources: t.Iterable[Source]

    # 3 Stages of the DW: "raw", "internal", and "output"
    raw_datastore: DatastoreBase
    internal_datastore: DatastoreBase
    output_datastore: DatastoreBase

    # Reverse EL flows that should run after the DW is ready.
    output_flows = t.Iterable[ELDataFlow]

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

    # Reverse EL

    def as_extractor(self) -> Extractor:
        """Return this data stack as an extractor."""
        return Extractor(self)

    # Actions

    @property
    def aspects(self) -> dict:
        """Aspects of this data stack."""
        return {
            "name": self.name,
            "naming_convention": self.naming_convention,
            "sql_staging_transforms": self.sql_staging_transforms,
            "sql_transforms": self.sql_transforms,
            "sources": self.sources,
            "storage_scheme": self.storage_scheme,
            "output_flows": self.output_flows,
        }

    def compile(self) -> None:
        """Compile the data stack."""
        for entity in self.entities.values():
            entity.compile()

    @classmethod
    def build(cls) -> None:
        """Build the data stack."""
        stack = cls()
        print(repr(stack.aspects))

    def publish(self) -> None:
        """Publish the data stack."""
        for entity in self.entities.values():
            entity.publish()
