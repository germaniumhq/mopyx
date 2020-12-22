from typing import List, Optional

from germanium_build_monitor.model.JenkinsJobBranch import JenkinsJobBranch
from germanium_build_monitor.model.JenkinsJobBranchBuild import JenkinsJobBranchBuild
from germanium_build_monitor.model.BuildStatus import BuildStatus
from germanium_build_monitor.model.Notification import Notification


def compare_branches(initial_branches: List[JenkinsJobBranch],
                     updated_branches: List[JenkinsJobBranch]):
    notifications = []

    for branch in updated_branches:
        if not find_branch(initial_branches, branch):
            if branch.status == BuildStatus.SUCCESS or branch.status == BuildStatus.FAILURE:
                last_build = get_last_finished_build(branch)

                if last_build:
                    notifications.append(Notification(branch, last_build))

    for initial_branch in initial_branches:
        updated_branch = find_branch(updated_branches, initial_branch)

        if not updated_branch:
            continue

        if len(updated_branch.builds) != len(initial_branch.builds):
            last_build = get_last_finished_build(updated_branch)
            assert last_build

            if last_build.status == BuildStatus.SUCCESS or last_build.status == BuildStatus.FAILURE:
                notifications.append(Notification(updated_branch, last_build))  # FIXME: state changes only?

            continue

        # FIXME: foreach on the branch builds, matching on build number?
        if updated_branch.builds:  # same number of builds, maybe some of it finished
            last_known_build = get_last_finished_build(initial_branch)
            last_updated_build = get_last_finished_build(updated_branch)

            if not last_known_build:
                continue

            assert last_updated_build

            if last_known_build.status != last_updated_build.status:
                notifications.append(Notification(updated_branch, last_updated_build))

    return notifications


def find_branch(branch_list: List[JenkinsJobBranch],
                searched_branch: JenkinsJobBranch) -> Optional[JenkinsJobBranch]:

    for branch in branch_list:
        if branch.branch_name == searched_branch.branch_name:
            return branch

    return None


def get_last_finished_build(branch: JenkinsJobBranch) -> Optional[JenkinsJobBranchBuild]:
    if not branch.builds:
        return None

    return branch.builds[0]

