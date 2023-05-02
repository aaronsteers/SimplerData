import abc
from enum import Enum, auto

from simpler.properties import DataProperty


class AggregationMethodEnum(Enum):
    FIRST = auto()
    LAST = auto()
    SUM = auto()
    AVERAGE = auto()
    MIN = auto()
    MAX = auto()
    COUNT = auto()
    COUNT_DISTINCT = auto()


class AggregationCalc:
    """An aggregation method."""

    method: AggregationMethodEnum
    over: list[DataProperty]


class AnalysisCalc(abc.ABCMeta):
    """An analysis calculation."""

    name: str
    inputs: list[DataProperty]
    time_period_aggregation: AggregationCalc


class AggregationCalc(AnalysisCalc):
    """An aggregation calculation."""

    name: str
    property: DataProperty

    def __init__(self, property: DataProperty):
        self.property = property

    def inputs(self) -> list[DataProperty]:
        return [self.property]
