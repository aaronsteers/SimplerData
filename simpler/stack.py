import abc
import typing as t
from functools import cached_property

from simpler.connectors import Extractor, Source
from simpler.entities import DataEntity
from simpler.flows import ELDataFlow
from simpler.naming import NamingConvention
from simpler.stores import DatastoreBase
from simpler.tables import SourceTable
from simpler.transforms._aggregate import AnalysisCalc
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

    # Reverse ETL flows that should run after the DW is ready.
    publish_flows = t.Iterable[ELDataFlow]

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

    def compile(self) -> None:
        """Compile the data stack."""
        for entity in self.entities.values():
            entity.compile()

    def build(self) -> None:
        """Build the data stack."""
        for entity in self.entities.values():
            entity.build()

    def publish(self) -> None:
        """Publish the data stack."""
        for entity in self.entities.values():
            entity.publish()
