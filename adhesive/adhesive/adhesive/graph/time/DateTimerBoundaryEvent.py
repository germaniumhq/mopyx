import datetime
import time

from adhesive.graph.time.ParsedDateDefinition import ParsedDateDefinition
from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent


class DateTimerBoundaryEvent(TimerBoundaryEvent[ParsedDateDefinition]):
    def __init__(self,
                 *,
                 parent_process: 'Process',
                 id: str,
                 name: str,
                 expression: str) -> None:
        super(DateTimerBoundaryEvent, self).__init__(
            parent_process=parent_process,
            id=id,
            name=name
        )

        self.definition = ParsedDateDefinition.from_str(expression)

    def total_seconds(self) -> int:
        # Currently we're computing a seconds offset to find out
        # when to fire the event.
        now = time.time()
        date_seconds = (self.definition.date - datetime.datetime(1970,1,1)).total_seconds()

        return date_seconds - now


from adhesive.graph.Process import Process
