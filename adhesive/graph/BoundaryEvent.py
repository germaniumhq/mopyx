from adhesive.graph.Event import Event
import adhesive


class BoundaryEvent(Event):
    def __init__(self,
                 *,
                 parent_process: 'adhesive.graph.Process.Process',
                 id: str,
                 name: str) -> None:
        super(BoundaryEvent, self).__init__(
            parent_process=parent_process,
            id=id,
            name=name)

        self.attached_task_id = 'not attached'

        self.cancel_activity = True
        self.parallel_multiple = False
