from typing import List, Dict, Union

from adhesive.execution.ExecutionLane import ExecutionLane
from adhesive.execution.ExecutionMessageCallbackEvent import ExecutionMessageCallbackEvent
from adhesive.execution.ExecutionMessageEvent import ExecutionMessageEvent
from adhesive.execution.ExecutionTask import ExecutionTask
from adhesive.execution.ExecutionUserTask import ExecutionUserTask
from adhesive.graph.Process import Process
from .AdhesiveLane import AdhesiveLane


class AdhesiveProcess:
    """
    An Adhesive process. Holds the linkage between
    the graph, and the steps.
    """
    def __init__(self, id: str) -> None:
        self.lane_definitions: List[ExecutionLane] = []
        self.task_definitions: List[ExecutionTask] = []
        self.user_task_definitions: List[ExecutionUserTask] = []
        self.message_definitions: List[ExecutionMessageEvent] = []
        self.message_callback_definitions: List[ExecutionMessageCallbackEvent] = []

        self.chained_task_definitions: List[Union[ExecutionTask, ExecutionUserTask]] = []

        self.process: Process = Process(id=id)

        # map from lane key, to actual lane
        self.lanes: Dict[str, AdhesiveLane] = dict()
