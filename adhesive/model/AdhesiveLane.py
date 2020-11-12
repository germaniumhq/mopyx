from typing import Any, Optional

import logging

from adhesive.workspace.Workspace import Workspace
from adhesive.execution.ExecutionLaneId import ExecutionLaneId

LOG = logging.getLogger(__name__)


class AdhesiveLane:
    """
    An active lane used in a process.
    """
    def __init__(
            self,
            lane_id: ExecutionLaneId,
            workspace: Workspace,
            generator: Any,
            parent_lane: Optional['AdhesiveLane'] = None) -> None:
        self.lane_id = lane_id
        self.workspace = workspace
        self.generator = generator
        self.references = 0
        self.parent_lane = parent_lane

    def deallocate_lane(self) -> None:
        LOG.debug(f"Lane: destroying lane {self.lane_id}")
        type(self.generator).__exit__(self.generator, None, None, None)

    def increment_references(self) -> None:
        self.references += 1
        LOG.debug(f"Lane: incremented references {self}")

        if self.parent_lane:
            self.parent_lane.increment_references()

    def decrement_references(self) -> None:
        self.references -= 1
        LOG.debug(f"Lane: decremented references {self}")

        if self.parent_lane:
            self.parent_lane.decrement_references()

    def __repr__(self) -> str:
        return f"AdhesiveLane({self.lane_id.key}, references={self.references})"
