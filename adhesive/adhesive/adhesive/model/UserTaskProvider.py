import adhesive
from adhesive.model.ActiveEvent import ActiveEvent

import abc


class UserTaskProvider:
    @abc.abstractmethod
    def register_event(self,
                       executor: 'adhesive.model.ProcessExecutor.ProcessExecutor',
                       event: ActiveEvent) -> None:
        pass
