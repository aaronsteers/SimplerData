import abc

from simpler.tables import SourceTable, Table


class SQLTransformBase(metaclass=abc.ABCMeta):
    """A SQL transform."""

    input_tables: list[Table]
    sql: str


class SQLTransform(SQLTransformBase):
    """A SQL transform."""

    input_tables: list[Table]
    sql: str

    def __init__(self, /, tables: list[Table]):
        """Initialize the transform."""
        self.tables = tables


class SQLStageTransform(SQLTransform):
    """A SQL staging transform."""

    source_table: SourceTable

    def __init__(self, /, source_table: Table):
        """Initialize the staging transform."""
        self.source_table = source_table
        super().__init__([source_table])

    def input_tables(self) -> list[Table]:
        """Return the input tables for this transform."""
        return [self.source_table]

    @property
    def sql(self) -> str:
        """SQL for this transform."""
        return f"SELECT * FROM {self.source_table.name}"
