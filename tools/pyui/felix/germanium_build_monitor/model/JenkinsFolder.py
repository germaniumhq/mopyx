from typing import Optional

from typing import List
from mopyx import model

from .Selection import Selection


@model
class JenkinsFolder:
    def __init__(self,
                 parent: Optional['JenkinsFolder'],
                 name: str) -> None:
        super().__init__()

        self.name = name
        self.parent = parent

        self.selected = Selection.UNSELECTED
        self.folders: List['JenkinsFolder'] = []
        self.jobs: List[JenkinsJob] = []

    def as_dict(self):
        return {
            "name": self.name,
            "type": "JenkinsFolder",
            "folders": [x.as_dict() for x in self.folders],
            "jobs": [x.as_dict() for x in self.jobs],
        }


from .JenkinsJob import JenkinsJob
