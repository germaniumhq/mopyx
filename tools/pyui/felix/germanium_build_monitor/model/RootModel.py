from typing import List, cast, Dict, Any

from mopyx import model, computed

from .JenkinsServer import JenkinsServer
from .Systray import Systray
from .BuildStatus import BuildStatus


@model
class RootModel:
    """
    Root model of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        self.search_text: str = ""
        self.servers: List[JenkinsServer] = []
        self.systray: Systray = Systray()

    @computed
    def status(self) -> BuildStatus:
        result = BuildStatus.NEVER

        for server in self.servers:
            for monitored_job in server.monitored_jobs:
                if not monitored_job.branches:
                    continue

                for branch in monitored_job.branches:
                    if branch.status == BuildStatus.RUNNING:
                        return BuildStatus.RUNNING
                    elif branch.status == BuildStatus.SUCCESS and result == BuildStatus.NEVER:
                        result = BuildStatus.SUCCESS
                    elif branch.status == BuildStatus.FAILURE:
                        result = BuildStatus.FAILURE

        return result

    @computed
    def last_known_status(self) -> BuildStatus:
        result = BuildStatus.NEVER

        for server in self.servers:
            for monitored_job in server.monitored_jobs:
                if not monitored_job.branches:
                    continue

                for branch in monitored_job.branches:
                    if branch.last_known_status == BuildStatus.SUCCESS and result == BuildStatus.NEVER:
                        result = BuildStatus.SUCCESS
                    elif branch.last_known_status == BuildStatus.FAILURE:
                        result = BuildStatus.FAILURE

        return result

    def as_dict(self) -> Dict[str, Any]:
        return {
            "search_text": self.search_text,
            "servers": [server.as_dict() for server in self.servers]
        }

    @staticmethod
    def from_dict(d) -> 'RootModel':
        result = RootModel()

        result.search_text = d.get("search_text", "")
        result.servers = [JenkinsServer.from_dict(s) for s in d['servers']]

        return result


root_model = cast(RootModel, RootModel())

