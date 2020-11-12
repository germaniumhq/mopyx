from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent
from adhesive.graph.time.ParsedDurationDefinition import ParsedDurationDefinition


class DurationTimerBoundaryEvent(TimerBoundaryEvent[ParsedDurationDefinition]):
    def __init__(self,
                 *,
                 parent_process: 'Process',
                 id: str,
                 name: str,
                 expression: str) -> None:
        super(DurationTimerBoundaryEvent, self).__init__(
            parent_process=parent_process,
            id=id,
            name=name
        )

        self.definition = ParsedDurationDefinition.from_str(expression)

    def total_seconds(self) -> int:
        # Currently we're computing a seconds offset to find out
        # when to fire the event.
        return self.definition.second + \
            self.definition.minute * 60 + \
            self.definition.hour * 3600 + \
            self.definition.day * 3600 * 24

from adhesive.graph.Process import Process
