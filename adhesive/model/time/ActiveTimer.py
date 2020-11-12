from typing import Optional, Callable

import schedule

from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent
from adhesive.model.ActiveEvent import ActiveEvent


class ActiveTimer:
    def __init__(self,
                 *,
                 fire_timer: Callable[[ActiveEvent, TimerBoundaryEvent], None],
                 parent_token: ActiveEvent,
                 timer_boundary_event: TimerBoundaryEvent) -> None:
        self.fire_timer = fire_timer
        self.parent_token = parent_token

        self.timer_boundary_event = timer_boundary_event
        self.job = schedule\
            .every(timer_boundary_event.total_seconds())\
            .seconds\
            .tag(parent_token.token_id)\
            .do(self.timer_triggered)

    def timer_triggered(self) -> Optional[schedule.CancelJob]:
        self.fire_timer(self.parent_token, self.timer_boundary_event)
        return None