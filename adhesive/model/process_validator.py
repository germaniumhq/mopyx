import logging
import sys
from typing import Optional, Dict, Union

from adhesive.execution.ExecutionUserTask import ExecutionUserTask
from adhesive.execution.ExecutionTask import ExecutionTask
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.execution.ExecutionMessageEvent import ExecutionMessageEvent
from adhesive.execution.ExecutionLane import ExecutionLane
from adhesive.execution.ExecutionMessageCallbackEvent import ExecutionMessageCallbackEvent

from adhesive.execution import token_utils

from adhesive.graph.Event import Event
from adhesive.graph.Gateway import Gateway
from adhesive.graph.Process import Process
from adhesive.graph.ScriptTask import ScriptTask
from adhesive.graph.SubProcess import SubProcess
from adhesive.graph.Task import Task
from adhesive.graph.UserTask import UserTask
from adhesive.model.generate_methods import display_unmatched_items, MatchableItem


LOG = logging.getLogger(__name__)


def _validate_tasks(self: 'ProcessExecutor',
                    process: Process,
                    missing_dict: Optional[Dict[str, MatchableItem]] = None) -> None:
    """
    Recursively traverse the graph, and print to the user if it needs to implement
    some tasks.

    :param process:
    :return:
    """
    unmatched_items: Dict[str, MatchableItem]

    if missing_dict is not None:
        unmatched_items = missing_dict
    else:
        unmatched_items = dict()

    for task_id, task in process.tasks.items():
        if isinstance(task, SubProcess):
            _validate_tasks(self, task, unmatched_items)
            continue

        # gateways don't have associated tasks with them.
        if isinstance(task, Event) or \
                isinstance(task, Gateway):
            continue

        if isinstance(task, ScriptTask):
            if task.language in ("python", "text/python", "python3", "text/python3"):
                continue

            raise Exception(f"Unknown script task language: {task.language}. Only python and "
                            f"text/python are supported.")

        if isinstance(task, Task):
            adhesive_task = _match_task(self, task)

            if not adhesive_task:
                unmatched_items[f"task:{task.name}"] = task
                continue

            self.tasks_impl[task_id] = adhesive_task

            # we copy the deduplication expression
            task.deduplicate = adhesive_task.deduplicate

            adhesive_task.used = True
            continue

        if isinstance(task, UserTask):
            adhesive_user_task = _match_user_task(self, task)

            if not adhesive_user_task:
                unmatched_items[f"usertask:{task.name}"] = task
                continue

            self.user_tasks_impl[task_id] = adhesive_user_task

            # we copy the deduplication expression
            task.deduplicate = adhesive_user_task.deduplicate

            adhesive_user_task.used = True
            continue

    for lane_id, lane in process.lanes.items():
        lane_definition = _match_lane(self, lane.name)

        if not lane_definition:
            unmatched_items[f"lane:{lane.name}"] = lane
            continue

        lane_definition.used = True

    for mevent_id, message_event in process.message_events.items():
        message_event_definition = _match_message_event(self, message_event.name)

        if not message_event_definition:
            unmatched_items[f"message_event:{message_event.name}"] = message_event
            continue

        if isinstance(message_event_definition, ExecutionMessageEvent):
            self.mevent_impl[mevent_id] = message_event_definition
        else:
            self.mevent_callback_impl[mevent_id] = message_event_definition

        message_event_definition.used = True

    if missing_dict is not None:  # we're not the root call, we're done
        return

    # The default lane is not explicitly present in the process. If we have
    # an implementation, we don't want to see it as an unused warning.
    lane_definition = _match_lane(self, "default")
    # if we don't have a definition, the lane_controller will dynamically add
    # it.
    # FIXME: probably it's better if the lane definition would be here.
    if lane_definition:
        lane_definition.used = True

    for task_definition in self.adhesive_process.task_definitions:
        if not task_definition.used:
            LOG.warning(f"Unused task: {task_definition}")

    for user_task_definition in self.adhesive_process.user_task_definitions:
        if not user_task_definition.used:
            LOG.warning(f"Unused usertask: {user_task_definition}")

    for lane_definition in self.adhesive_process.lane_definitions:
        if not lane_definition.used:
            LOG.warning(f"Unused lane: {lane_definition}")

    for execution_message_event in self.adhesive_process.message_definitions:
        if not execution_message_event.used:
            LOG.warning(f"Unused message: {execution_message_event}")

    for message_event_callback in self.adhesive_process.message_callback_definitions:
        if not message_event_callback.used:
            LOG.warning(f"Unused message: {message_event_callback}")

    if unmatched_items:
        display_unmatched_items(unmatched_items.values())
        sys.exit(1)


def _match_task(self, task: ProcessTask) -> Optional[ExecutionTask]:
    for task_definition in self.adhesive_process.task_definitions:
        if token_utils.matches(task_definition.re_expressions, task.name) is not None:
            return task_definition

    return None


def _match_user_task(self, task: ProcessTask) -> Optional[ExecutionUserTask]:
    for task_definition in self.adhesive_process.user_task_definitions:
        if token_utils.matches(task_definition.re_expressions, task.name) is not None:
            return task_definition

    return None


def _match_lane(self, lane_name: str) -> Optional[ExecutionLane]:
    for lane_definition in self.adhesive_process.lane_definitions:
        if token_utils.matches(lane_definition.re_expressions, lane_name) is not None:
            return lane_definition

    return None


def _match_message_event(self, message_event_name: str) -> Optional[
    Union[ExecutionMessageEvent, ExecutionMessageCallbackEvent]]:
    for message_definition in self.adhesive_process.message_definitions:
        if token_utils.matches(message_definition.re_expressions, message_event_name) is not None:
            return message_definition

    for message_callback_definition in self.adhesive_process.message_callback_definitions:
        if token_utils.matches(message_callback_definition.re_expressions, message_event_name) is not None:
            return message_callback_definition

    return None

from adhesive.model.ProcessExecutor import ProcessExecutor