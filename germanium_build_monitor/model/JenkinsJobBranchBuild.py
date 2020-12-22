from mopyx import model

from .BuildStatus import BuildStatus


@model
class JenkinsJobBranchBuild:
    def __init__(self,
                 name: str,
                 status: BuildStatus,
                 url: str,
                 timestamp: int,
                 building: bool) -> None:
        self.name = name
        self.status = status
        self.url = url
        self.timestamp = timestamp
        self.building = building
