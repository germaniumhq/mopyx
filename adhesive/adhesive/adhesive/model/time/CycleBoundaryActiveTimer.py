from typing import Optional, Callable

import schedule

from adhesive.graph.time.CycleTimerBoundaryEvent import CycleTimerBoundaryEvent
from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent
from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.model.time.ActiveTimer import ActiveTimer


class CycleBoundaryActiveTimer(ActiveTimer):
    def __init__(self,
                 *,
                 parent_token: ActiveEvent,
                 fire_timer=Callable[[ActiveEvent, TimerBoundaryEvent], None],
                 timer_boundary_event: CycleTimerBoundaryEvent):
        super(CycleBoundaryActiveTimer, self).__init__(
            parent_token=parent_token,
            fire_timer=fire_timer,
            timer_boundary_event=timer_boundary_event
        )

        self.execution_count = 0

    def timer_triggered(self) -> Optional[schedule.CancelJob]:
        super(CycleBoundaryActiveTimer, self).timer_triggered()

        self.execution_count += 1
        if self.timer_boundary_event.definition.repeat_count < 0:
            return None

        if self.execution_count >= self.timer_boundary_event.definition.repeat_count:
            return schedule.CancelJob

        return None