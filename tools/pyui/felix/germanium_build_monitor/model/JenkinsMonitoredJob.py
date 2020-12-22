from typing import List, Optional, Dict, Any, Set
from mopyx import model, action


@model
class JenkinsMonitoredJob:
    def __init__(self,
                 name: str,
                 full_name: Optional[str] = None,
                 ignored_branches: Optional[Set[str]] = None):
        self.name: str = name
        self.full_name: str = full_name if full_name else name
        self.branches: Optional[List[JenkinsJobBranch]] = None
        self.ignored_branches: Set[str] = ignored_branches if ignored_branches else set()
        self.url: str = ""  # needs to be fetched from builds
        self.failed_count = 0

    @action
    def set_ignored_branch(self, branch, ignored: bool) -> None:
        if ignored:
            self.ignored_branches.add(branch.branch_name)
        else:
            self.ignored_branches.remove(branch.branch_name)

        self.ignored_branches = self.ignored_branches

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "full_name": self.full_name,
            "ignored_branches": self.ignored_branches,
        }

    @staticmethod
    def from_dict(d) -> 'JenkinsMonitoredJob':
        return JenkinsMonitoredJob(
            name=d["name"],
            full_name=d["full_name"],
            ignored_branches=d.get("ignored_branches", set())
        )


from .JenkinsJobBranch import JenkinsJobBranch
