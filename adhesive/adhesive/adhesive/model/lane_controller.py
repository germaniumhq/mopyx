import logging
from typing import Optional, Any, Generator

from adhesive.execution.ExecutionToken import ExecutionToken

import adhesive
from adhesive.execution import token_utils
from adhesive.execution.ExecutionLaneId import ExecutionLaneId
from adhesive.graph.Process import Process
from adhesive.workspace.Workspace import Workspace
from adhesive.workspace.local.LocalLinuxWorkspace import LocalLinuxWorkspace
from .ActiveEvent import ActiveEvent
from .AdhesiveLane import AdhesiveLane
from .AdhesiveProcess import AdhesiveProcess

LOG = logging.getLogger(__name__)

DEFAULT_LANE_ID = ExecutionLaneId("root", "default")


def ensure_default_lane(process: AdhesiveProcess) -> None:
    """
    Ensures the 'default' lane is defined.
    """
    if DEFAULT_LANE_ID.key in process.lanes:
        return

    @adhesive.lane('default')
    def lane_default(context: adhesive.Token) -> adhesive.WorkspaceGenerator:
        yield context.workspace


def allocate_workspace(process: AdhesiveProcess,
                       event: ActiveEvent) -> None:
    """
    Allocates a workspace. This matches against the available lanes,
    and creates the workspace.
    """
    LOG.debug(f"Lane allocate workspace check for {event}")

    original_execution_lane_id = event.context.lane
    fill_in_lane_id(process, event)

    lane = find_existing_lane_for_event(process, event)

    if not lane:
        LOG.debug(f"Crating a new lane for {event}")
        lane = create_lane_for_event(process, event, original_execution_lane_id)

    lane.increment_references()

    event.context.workspace = lane.workspace.clone()


def deallocate_workspace(process: AdhesiveProcess,
                         event: ActiveEvent) -> None:
    """
    Deallocates a workspace. This also checks for potentially the need
    to destroy workspaces (including parent ones)
    """
    LOG.debug(f"Lane deallocate workspace check for {event}")

    lane = find_existing_lane_for_event(process, event)

    if not lane:
        raise Exception(f"Unable to find lane for {event} on lane {event.context.lane}")

    lane.decrement_references()

    while lane and lane.references == 0:
        parent_lane = lane.parent_lane

        lane.deallocate_lane()
        del process.lanes[lane.lane_id.key]

        lane = parent_lane


def fill_in_lane_id(process: AdhesiveProcess,
                    event: ActiveEvent) -> None:
    """
    Ensures the lane_id is not the cloned one, but the one where the task
    resides.
    """
    parent_process = None

    if hasattr(event.task, "parent_process"):
        parent_process = event.task.parent_process

    # FIXME: if we don't have a `parent_process` the current event should
    # target the root process. Not sure why the `isinstance` is still necessary,
    if not parent_process and isinstance(event.task, Process):
        parent_process = event.task

    assert parent_process

    lane_definition = parent_process.get_lane_definition(event.task.id)

    event.context.lane = ExecutionLaneId(
            lane_id=lane_definition.id,
            lane_name=lane_definition.name)


def find_existing_lane_for_event(process: AdhesiveProcess,
                                 event: ActiveEvent) -> Optional[AdhesiveLane]:
    """
    Finds out the lane for an event (if it exists). This function
    happens after the `fill_lane_id` in the `allocate_workspace`, or
    in `deallocate_workspace`, so at this stage we always have a
    lane.
    """
    assert event.context.lane

    if event.context.lane.key not in process.lanes:
        return None

    return process.lanes[event.context.lane.key]


def create_lane_for_event(process: AdhesiveProcess,
                          event: ActiveEvent,
                          execution_lane_id: Optional[ExecutionLaneId]) -> AdhesiveLane:
    """
    Creates the lane object and the associated workspace. Happens
    in the `allocate_workspace` after the `fill_lane_id` se we're guaranteed to
    have an assigned lane.
    """
    assert event.context.lane

    for lane_definition in process.lane_definitions:
        params = token_utils.matches(lane_definition.re_expressions,
                                     event.context.lane.name)

        if params is None:
            continue

        if not execution_lane_id or DEFAULT_LANE_ID.key == execution_lane_id.key:
            # The very first lane won't have any workspace. Since a lot of times we
            # just want to change the folder, we ensure that the default lane gets
            # the local workspace.
            # FIXME make it configurable?
            event.context.workspace = create_default_workspace(event.context)

        # create the lane object using the context
        gen = lane_definition.code(event.context, *params)

        workspace = type(gen).__enter__(gen)

        if not isinstance(workspace, Workspace):
            raise Exception(f"The lane yielded the wrong type {type(workspace)} instead of a Workspace")

        parent_lane: Optional[AdhesiveLane] = None

        # We have to create the lane being called from a different lane?
        if execution_lane_id and execution_lane_id.key != DEFAULT_LANE_ID.key:
            parent_lane = process.lanes[execution_lane_id.key]

        lane = AdhesiveLane(
            lane_id=event.context.lane,
            workspace=workspace,
            generator=gen,
            parent_lane=parent_lane)

        process.lanes[event.context.lane.key] = lane

        return lane

    raise Exception(
            f"Unable to find any definition for lane "
            f"`{event.context.lane.name}`. Use the @adhesive.lane "
            f"decorator to create them, and yield the workspace.")


def create_default_workspace(context) -> Workspace:
    return LocalLinuxWorkspace(context.execution_id, context.token_id)