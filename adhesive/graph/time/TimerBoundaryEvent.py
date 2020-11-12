import abc
from typing import Generic, TypeVar

from adhesive.graph.BoundaryEvent import BoundaryEvent

TimeDefinition = TypeVar('TimeDefinition')


class TimerBoundaryEvent(BoundaryEvent, Generic[TimeDefinition], metaclass=abc.ABCMeta):
    definition: TimeDefinition

    """
    A base class for all the timer boundary events
    """
    @abc.abstractmethod
    def total_seconds(self) -> int: ...
