from typing import Optional

import schedule

from adhesive.model.time.ActiveTimer import ActiveTimer


class DateBoundaryActiveTimer(ActiveTimer):
    def timer_triggered(self) ->  Optional[schedule.CancelJob]:
        super(DateBoundaryActiveTimer, self).timer_triggered()

        return schedule.CancelJob
