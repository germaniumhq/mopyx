import copy
import logging
import uuid
from concurrent.futures import Future
from typing import Optional

from adhesive import config
from adhesive.consoleui.color_print import red
from adhesive.execution import token_utils
from adhesive.execution.ExecutionLoop import loop_id
from adhesive.graph.ExecutableNode import ExecutableNode
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.model.ActiveEventStateMachine import ActiveEventState
from adhesive.model.ActiveLoopType import ActiveLoopType

LOG = logging.getLogger(__name__)

DONE_STATES = {
    ActiveEventState.DONE_CHECK,
    ActiveEventState.DONE_END_TASK,
    ActiveEventState.DONE,
}

ACTIVE_STATES = {
    ActiveEventState.NEW,
    ActiveEventState.PROCESSING,
    ActiveEventState.WAITING,
    ActiveEventState.RUNNING,
    ActiveEventState.ERROR,
    ActiveEventState.ROUTING,
}

# When waiting for predecessors it only makes sense to collapse events
# into ActiveEvents only when the event is not already running.
PRE_RUN_STATES = {
    ActiveEventState.NEW,
    ActiveEventState.PROCESSING,
    ActiveEventState.WAITING,
}


class ActiveEvent:
    """
    An event that passes through the system. It can fork
    in case there are multiple executions going down.
    """
    def __init__(self,
                 execution_id: str,
                 parent_id: Optional['str'],
                 context: 'ExecutionToken',
                 deduplication_id: Optional[str] = None
            ) -> None:
        self.execution_id = execution_id
        self.token_id: str = str(uuid.uuid4())
        self.parent_id = parent_id

        self.deduplication_id = deduplication_id
        self.deduplication_registered = False
        self.deduplication_unregistered = False

        if not isinstance(context, ExecutionToken):
            raise Exception(f"Not an execution token: {context}")

        self._task = context.task
        self.context = context

        self.state = ActiveEventState.NEW
        self.future: Optional[Future] = None

        self.loop_type: Optional[ActiveLoopType] = None
        self._next_event: Optional['ActiveEvent'] = None

    def __getstate__(self):
        return {
            "execution_id": self.execution_id,
            "token_id": self.token_id,
            "parent_id": self.parent_id,
            "deduplication_id": self.deduplication_id,
            "_task": self._task,
            "context": self.context
        }

    def clone(self,
              task: ExecutableNode,
              parent_id: Optional[str]) -> 'ActiveEvent':
        """
        Clone the current event for another task id target.
        """
        result = ActiveEvent(
            execution_id=self.execution_id,
            parent_id=parent_id,  # FIXME: why, if this is a clone
            context=self.context.clone(task),
            deduplication_id=self.deduplication_id,
        )
        result.context.token_id = result.token_id

        # if we are exiting the current loop, we need to switch to the
        # parent loop.
        # FIXME: this probably doesn't belong here
        # FIXME: the self.task != task is probably wrong, since we want to support
        # boolean looping expressions.

        # only ProcessTasks have loops.
        if isinstance(self.context.task, ProcessTask) \
                and self.context.task.loop \
                and self.context.loop \
                and self.context.loop.task == self.context.task \
                and self.context.task != task \
                and parent_id == self.parent_id:
            result.context.loop = self.context.loop.parent_loop
        else:
            result.context.loop = self.context.loop

        result.context._update_title_from_data()

        return result

    @property
    def task(self) -> ExecutableNode:
        return self._task

    @task.setter
    def task(self, task: ProcessTask) -> None:
        if not isinstance(task, ProcessTask):
            raise Exception(f"Not a task: {task}")

        self.context.task = task
        self._task = task

    def __repr__(self) -> str:
        # the task.token_id should be the same as the self.execution.token_id
        if self.deduplication_id:
            return f"ActiveEvent({self.token_id}, {self.state}): " \
                   f"({self.deduplication_id}:{self.task.id}):{self.context.task_name}"

        return f"ActiveEvent({self.token_id}, {self.state}): " \
               f"({self.task.id}):{self.context.task_name}"


def is_parent(self,
              *,
              parent_element: ActiveEvent,
              child_element: ActiveEvent) -> bool:
    parent_id = child_element.parent_id

    while parent_id:
        if parent_id == parent_element.token_id:
            return True

        parent_id = self.events[parent_id].parent_id

    return False


def is_potential_predecessor(self, event: ActiveEvent, e: ActiveEvent) -> bool:
    # if the events are not in the same process they're not related
    if event.parent_id != e.parent_id:
        return False

    if e.state not in ACTIVE_STATES:
        return False

    if e.task == event.task:
        return False

    # When we have a loop on an element, if it's already running (i.e. not
    # initial), it means we already evaluated we don't have any predecessors
    if event.context.loop and \
            event.context.loop.task.id == event.task.id and \
            event.context.loop.index >= 0:
        return False

    return loop_id(e) == loop_id(event)


def deep_copy_event(e: ActiveEvent) -> ActiveEvent:
    """
    We deepcopy everything except the workspace.
    :param e:
    :return:
    """
    try:
        workspace = e.context.workspace
        e.context.workspace = None
        result = copy.deepcopy(e)

        result.context.workspace = workspace

        return result
    except Exception as err:
        LOG.error(red("Unable to serialize token", bold=True))
        LOG.error(red(f"Data: {e.context.data._data}"))
        raise err


def noop_copy_event(e: ActiveEvent) -> ActiveEvent:
    return e


copy_event = noop_copy_event \
        if config.current.parallel_processing == "process" else \
        deep_copy_event


from adhesive.execution.ExecutionToken import ExecutionToken
