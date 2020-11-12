from typing import Callable, Any, Optional

import adhesive
from adhesive.execution import token_utils
from adhesive.graph.ProcessTask import ProcessTask


class SerialExecutionLoopState:
    def __init__(self) -> None:
        self.current_index = 0


class ExecutionLoop:
    """
    Holds the current looping information.
    """
    def __init__(self,
                 *args,
                 event_id: str,
                 parent_loop: Optional['ExecutionLoop'],
                 task: ProcessTask,
                 item: Any,
                 index: int,
                 expression: str,
             ) -> None:
        if args:
            raise Exception("You need to pass the parameters by name")

        self.event_id = event_id
        self._task = task
        self._key = item
        self._value = item
        self._index = index
        self.parent_loop = parent_loop
        self._expression = expression

    @property
    def task(self) -> ProcessTask:
        return self._task

    @property
    def key(self) -> Any:
        return self._key

    @property
    def item(self) -> Any:
        return self._value

    @property
    def value(self) -> Any:
        return self._value

    @property
    def index(self) -> int:
        return self._index

    @property
    def expression(self) -> str:
        return self._expression

    def __repr__(self) -> str:
        """
        String object representation
        """
        return f"Loop[ event_id: {self.event_id}, index: {self.index}, key: {self._key}, value: {self._value}"

    @staticmethod
    def create_loop(event: 'adhesive.model.ActiveEvent.ActiveEvent',
                    clone_event: Callable[['adhesive.model.ActiveEvent.ActiveEvent', 'ProcessTask'], 'adhesive.model.ActiveEvent.ActiveEvent'],
                    target_task: 'ProcessTask') -> int:
        assert target_task.loop

        expression = target_task.loop.loop_expression

        eval_data = token_utils.get_eval_data(event.context)
        result = eval(expression, {}, eval_data)

        if not result:
            return 0

        index = 0
        for item in result:
            new_event = clone_event(event, target_task)

            parent_loop = new_event.context.loop
            new_event.context.loop = ExecutionLoop(
                event_id=event.token_id,
                parent_loop=parent_loop,
                task=target_task,
                item=item,
                index=index,
                expression=expression)

            # if we're iterating over a map, we're going to store the
            # values as well.
            if isinstance(result, dict):
                new_event.context.loop._value = result[item]

            # FIXME: this knows way too much about how the ExecutionTokens are
            # supposed to function
            # FIXME: rename all event.contexts to event.token. Context is only
            # true in the scope of an execution task.
            new_event.context._update_title_from_data()

            index += 1

        return index


def parent_loop_id(e: 'adhesive.model.ActiveEvent.ActiveEvent') -> Optional[str]:
    if not e.context.loop:
        return None

    if not e.context.loop.parent_loop:
        return None

    return f"{e.context.loop.parent_loop.event_id}:{e.context.loop.parent_loop.index}"


def loop_id(event: 'adhesive.model.ActiveEvent.ActiveEvent') -> Optional[str]:
    """
    Finds the loop id where this event executes. This is the owning loop ID.
    :param event:
    :return:
    """
    loop: Optional[ExecutionLoop] = event.context.loop

    if not loop:
        return None

    if loop.task == event.context.task:
        loop = loop.parent_loop

    if not loop:
        return None

    return f"{loop.event_id}:{loop.index}"
