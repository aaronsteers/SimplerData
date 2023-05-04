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
    """An aggregation calculation."""

    method: AggregationMethodEnum
    over: list[DataProperty]


class AnalysisCalc:
    """An analysis calculation."""

    name: str
    inputs: list[DataProperty]
    time_period_aggregation: AggregationCalc
