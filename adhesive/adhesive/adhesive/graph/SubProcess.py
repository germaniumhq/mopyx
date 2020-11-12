from adhesive.graph.Lane import Lane
from adhesive.graph.Process import Process
from adhesive.graph.ProcessTask import ProcessTask


class SubProcess(ProcessTask, Process):
    def __init__(self,
                 *,
                 parent_process: Process,
                 id: str,
                 name: str):
        super(SubProcess, self).__init__(
            id=id,
            name=name,
            parent_process=parent_process)

    def get_lane_definition(self, task_id: str) -> Lane:
        assert self.parent_process
        return self.parent_process.get_lane_definition(self.id)
