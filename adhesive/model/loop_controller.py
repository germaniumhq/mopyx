import logging
import uuid
from typing import Any, cast, Optional

from adhesive.execution import token_utils
from adhesive.execution.ExecutionLoop import ExecutionLoop, SerialExecutionLoopState
from adhesive.graph.ProcessTask import ProcessTask
from .ActiveEvent import ActiveEvent
from .ActiveLoopType import ActiveLoopType

LOG = logging.getLogger(__name__)


def is_top_loop_event(event: ActiveEvent):
    return isinstance(event.task, ProcessTask) and \
           (not event.context.loop or event.context.loop.task != event.task)


def create_loop(event: ActiveEvent,
                clone_event,
                target_task: ProcessTask,
                parent_id: Optional[str] = None) -> None:
    """
    Create a loop event.
    """
    new_event = clone_event(event, target_task, parent_id=parent_id)

    assert new_event.context
    assert target_task.loop

    owning_loop = event.context.loop

    # FIXME: task check should have just worked
    if event.context.loop and \
        event.context.loop.task.id == event.task.id:
        owning_loop = event.context.loop.parent_loop

    new_event.loop_type = ActiveLoopType.INITIAL
    new_event.context.loop = ExecutionLoop(
        event_id=event.token_id,
        parent_loop=owning_loop,
        task=new_event.task,
        item=None,
        index=-1,
        expression=target_task.loop.loop_expression
    )


def evaluate_initial_loop(event: ActiveEvent, clone_event) -> None:
    """
    evals the initial expression of the loop and determines its type. If the
    expression returns a collection the loop creates all the events with a
    COLLECTION type. If it returns a truthy, the loop creates a single
    CONDITION event. If it's falsy, the current event changes to INITIAL_EMPTY.
    """
    assert isinstance(event.task, ProcessTask)
    assert event.task.loop
    assert event.context.loop

    LOG.debug(f"Loop: Evaluate a new loop: {event.task.loop.loop_expression}")
    loop_data = evaluate_loop_expression(event)

    if not loop_data:
        LOG.debug("Loop is INITIAL_EMPTY")
        event.loop_type = ActiveLoopType.INITIAL_EMPTY
        return

    if not is_collection(loop_data):
        return create_condition_loop(clone_event, event, loop_data)

    if event.task.loop.parallel:
        return create_collection_loop(clone_event, event, loop_data)

    return create_collection_serial_loop(clone_event, event, loop_data)


def create_condition_loop(clone_event, event, loop_data):
    LOG.debug(f"Loop: CONDITION loop for {event.context.loop.event_id}")

    new_event = clone_event(event, event.task)

    new_event.loop_type = ActiveLoopType.CONDITION

    assert new_event.context

    new_event.context.loop = ExecutionLoop(
        event_id=event.token_id,
        parent_loop=event.context.loop.parent_loop,
        task=cast(ProcessTask, event.task),
        item=loop_data,
        index=0,
        expression=event.task.loop.loop_expression)

    return


def create_collection_loop(clone_event, event, loop_data):
    LOG.debug(f"Loop: COLLECTION loop for {event.context.loop.event_id}")
    index = 0

    for item in loop_data:
        new_event = clone_event(event, event.task)

        assert new_event.context

        LOG.debug(f"Loop: parent loop {event.context.loop.parent_loop}")

        new_event.context.loop = ExecutionLoop(
            event_id=event.token_id,
            parent_loop=event.context.loop.parent_loop,
            task=cast(ProcessTask, event.task),
            item=item,
            index=index,
            expression=event.task.loop.loop_expression,
        )

        new_event.loop_type = ActiveLoopType.COLLECTION

        # if we're iterating over a map, we're going to store the
        # values as well.
        if isinstance(loop_data, dict):
            new_event.context.loop._value = loop_data[item]

        # FIXME: this knows way too much about how the ExecutionTokens are
        # supposed to function
        # FIXME: rename all event.contexts to event.token. Context is only
        # true in the scope of an execution task.
        LOG.debug(f"Loop value {new_event.context.loop.value}")

        index += 1


def create_collection_serial_loop(clone_event, event, loop_data):
    _next_event: Optional[ActiveEvent] = None

    LOG.debug(f"Loop: COLLECTION_SERIAL loop for {event.context.loop.event_id}")
    index = 0

    for item in loop_data:
        # we use the clone function only for the first event, since the events get
        # registered
        if _next_event:
            new_event = _next_event.clone(event.task, _next_event.parent_id)
        else:
            new_event = clone_event(event, event.task)

        assert new_event.context

        LOG.debug(f"Loop: parent loop {event.context.loop.parent_loop}")

        new_event.context.loop = ExecutionLoop(
            event_id=event.token_id,
            parent_loop=event.context.loop.parent_loop,
            task=cast(ProcessTask, event.task),
            item=item,
            index=index,
            expression=event.task.loop.loop_expression,
        )

        new_event.loop_type = ActiveLoopType.COLLECTION_SERIAL

        # if we're iterating over a map, we're going to store the
        # values as well.
        if isinstance(loop_data, dict):
            new_event.context.loop._value = loop_data[item]

        # FIXME: this knows way too much about how the ExecutionTokens are
        # supposed to function
        # FIXME: rename all event.contexts to event.token. Context is only
        # true in the scope of an execution task.
        LOG.debug(f"Loop value {new_event.context.loop.value}")

        index += 1

        if _next_event:
            _next_event._next_event = new_event
            _next_event = new_event
        else:
            _next_event = new_event


def is_conditional_loop_event(event: ActiveEvent) -> bool:
    """
    Checks the event if it's a conditional loop event.
    """
    return event.loop_type == ActiveLoopType.CONDITION


def next_conditional_loop_iteration(event: ActiveEvent, clone_event) -> bool:
    """
    evals the expression of the conditional loop event, to see if should still
    execute.
    """
    if event.loop_type != ActiveLoopType.CONDITION:
        return False

    result = evaluate_loop_expression(event)

    if not result:
        return False

    new_event = clone_event(event, event.task)
    new_event.loop_type = ActiveLoopType.CONDITION

    assert new_event.context
    assert event.context.loop

    new_event.context.loop = ExecutionLoop(
        event_id=event.token_id,
        parent_loop=event.context.loop.parent_loop,
        task=cast(ProcessTask, event.task),
        item=result,
        index=event.context.loop.index + 1,
        expression=event.context.loop.expression)

    return True


def is_collection(what: Any) -> bool:
    return hasattr(what, "__iter__")


def evaluate_loop_expression(event: ActiveEvent) -> Any:
    """
    Evaluates a loop expression.
    """
    assert isinstance(event.task, ProcessTask)
    assert event.task.loop

    eval_data = token_utils.get_eval_data(event.context)
    result = eval(event.task.loop.loop_expression, {}, eval_data)

    return result
