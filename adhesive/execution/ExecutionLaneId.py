
class ExecutionLaneId:
    """
    An identifier for a lane.
    """
    def __init__(self,
                 lane_id: str,
                 lane_name: str) -> None:
        self.id = lane_id
        self.name = lane_name

        self.key = f"{lane_id}:{lane_name}"

    def __repr__(self) -> str:
        return self.key
