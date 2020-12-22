from typing import Any, List

from germanium_build_monitor.model.JenkinsMonitoredJob import JenkinsMonitoredJob
from germanium_build_monitor.model.JenkinsJobBranch import JenkinsJobBranch
from germanium_build_monitor.model.JenkinsJobBranchBuild import JenkinsJobBranchBuild
from germanium_build_monitor.model.BuildStatus import BuildStatus


def read_build_job_branches(monitored_job: JenkinsMonitoredJob,
                            result: Any) -> List[JenkinsJobBranch]:
    monitored_job.url = result["url"]

    if result["_class"] == "org.jenkinsci.plugins.workflow.job.WorkflowJob":
        return [read_single_job_branch(monitored_job, result)]

    elif result["_class"] == "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject":
        branches = []

        for job in result["jobs"]:
            branch = read_single_job_branch(monitored_job, job)
            branches.append(branch)

        return branches
    else:
        raise Exception("Unsupported job type: " + str(result))


def read_single_job_branch(monitored_job: JenkinsMonitoredJob, job: Any) -> JenkinsJobBranch:
    branch_name = job["name"]
    url = job["url"]

    branch = JenkinsJobBranch(
        monitored_job=monitored_job,
        branch_name=branch_name,
        url=url)

    for build in job["builds"]:
        if build["building"]:
            build_status = BuildStatus.RUNNING
        elif build["result"] == "FAILURE":
            build_status = BuildStatus.FAILURE
        else:
            build_status = BuildStatus.SUCCESS

        # FIXME: duration, and estimatedDuration also available
        build_building = build["building"]
        build_timestamp = build["timestamp"]
        build_url = build["url"]
        build_name = build["displayName"]

        build = JenkinsJobBranchBuild(name=build_name,
                                      status=build_status,
                                      url=build_url,
                                      timestamp=build_timestamp,
                                      building=build_building)
        branch.builds.append(build)

    return branch


def status_from_color(color: str) -> BuildStatus:
    status = BuildStatus.SUCCESS if color == "blue" else BuildStatus.FAILURE
    return status

