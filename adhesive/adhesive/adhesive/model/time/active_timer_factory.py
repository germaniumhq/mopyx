from typing import Callable

from adhesive.graph.time.CycleTimerBoundaryEvent import CycleTimerBoundaryEvent
from adhesive.graph.time.DateTimerBoundaryEvent import DateTimerBoundaryEvent
from adhesive.graph.time.DurationTimerBoundaryEvent import DurationTimerBoundaryEvent
from adhesive.graph.time.TimerBoundaryEvent import TimerBoundaryEvent
from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.model.time.ActiveTimer import ActiveTimer
from adhesive.model.time.CycleBoundaryActiveTimer import CycleBoundaryActiveTimer
from adhesive.model.time.DateBoundaryActiveTimer import DateBoundaryActiveTimer
from adhesive.model.time.DurationBoundaryActiveTimer import DurationBoundaryActiveTimer


def create_active_timer(
        *,
        parent_token: ActiveEvent,
        boundary_event_definition: TimerBoundaryEvent,
        fire_timer: Callable[[ActiveEvent, TimerBoundaryEvent], None]) -> ActiveTimer:
    if isinstance(boundary_event_definition, DurationTimerBoundaryEvent):
        return DurationBoundaryActiveTimer(
            parent_token=parent_token,
            fire_timer=fire_timer,
            timer_boundary_event=boundary_event_definition)
    elif isinstance(boundary_event_definition, CycleTimerBoundaryEvent):
        return CycleBoundaryActiveTimer(
            parent_token=parent_token,
            fire_timer=fire_timer,
            timer_boundary_event=boundary_event_definition)
    elif isinstance(boundary_event_definition, DateTimerBoundaryEvent):
        return DateBoundaryActiveTimer(
            parent_token=parent_token,
            fire_timer=fire_timer,
            timer_boundary_event=boundary_event_definition)
    else:
        raise Exception(f"Wrong event definition sent to create a timer "
                        f"({boundary_event_definition}. "
                        f"Only Duration, Cycle and Date are supported.")
