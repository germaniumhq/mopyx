from .JenkinsJobBranch import JenkinsJobBranch
from .JenkinsJobBranchBuild import JenkinsJobBranchBuild


class Notification:
    def __init__(self,
                 branch: JenkinsJobBranch,
                 build: JenkinsJobBranchBuild):
        self.branch = branch
        self.build = build
