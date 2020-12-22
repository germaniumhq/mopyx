from typing import List, Optional

from mopyx import model, computed, action
import urllib.parse

from .BuildStatus import BuildStatus
from .JenkinsJobBranchBuild import JenkinsJobBranchBuild
from .JenkinsMonitoredJob import JenkinsMonitoredJob

from germanium_build_monitor.model import Settings


@model
class JenkinsJobBranch:
    def __init__(self,
                 monitored_job: JenkinsMonitoredJob,
                 branch_name: str,
                 url: str) -> None:
        self.parent_monitored_job = monitored_job
        self.branch_name = branch_name
        self.decoded_branch_name = urllib.parse.unquote(branch_name)
        self.builds: List[JenkinsJobBranchBuild] = []
        self.url: str = url

    @computed
    def sorted_builds(self) -> List[JenkinsJobBranchBuild]:
        result = list(self.builds)
        result.sort(key=lambda it: it.timestamp, reverse=True)

        return result

    @computed
    def project_name(self) -> str:
        return self.parent_monitored_job.name

    @computed
    def status(self) -> BuildStatus:
        if self.is_ignored:
            return BuildStatus.IGNORED

        if not self.sorted_builds:
            return BuildStatus.NEVER

        return self.sorted_builds[0].status

    @computed
    def last_known_status(self) -> BuildStatus:
        if self.status != BuildStatus.RUNNING:
            return self.status

        for build in self.sorted_builds:
            if build.status == BuildStatus.SUCCESS or build.status == BuildStatus.FAILURE:
                return build.status

        return BuildStatus.NEVER

    @computed
    def is_ignored(self) -> bool:
        return self.branch_name in self.parent_monitored_job.ignored_branches

    @action
    def set_ignored(self, ignored: bool) -> None:
        self.parent_monitored_job.set_ignored_branch(self, ignored)

    @computed
    def last_builds(self) -> List[JenkinsJobBranchBuild]:
        result = list(self.sorted_builds)
        result = result[0:Settings.settings.last_builds_count]

        return result

    @computed
    def last_build_timestamp(self) -> Optional[int]:
        if not self.builds:
            return None

        return max([build.timestamp for build in self.builds])

