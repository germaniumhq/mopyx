from typing import Optional

import schedule

from adhesive.model.time.ActiveTimer import ActiveTimer


class DurationBoundaryActiveTimer(ActiveTimer):
    def timer_triggered(self) -> Optional[schedule.CancelJob]:
        super(DurationBoundaryActiveTimer, self).timer_triggered()

        return schedule.CancelJob
