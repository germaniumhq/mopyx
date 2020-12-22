import unittest

from germanium_build_monitor.model.jenkins.remote.read_build_jobs import read_build_job_branches
from germanium_build_monitor.model.jenkins.operations import compare_branches

from .test_jenkins_build_loading import load_result
from germanium_build_monitor.model.JenkinsMonitoredJob import JenkinsMonitoredJob


class TestJobDifferencesInBuild(unittest.TestCase):
    """
    Checks if the notifications can be updated.
    """

    def test_new_branch_failure(self) -> None:
        """
        Checks the detection.
        """
        initial_run = load_result("jd_build_initial.json")
        initial_branches = read_build_job_branches(JenkinsMonitoredJob("jd"), initial_run)

        branch_rerun = load_result("jd_build_a_feature_wut_rerun.json")
        rerun_branches = read_build_job_branches(JenkinsMonitoredJob("jd"), branch_rerun)

        notifications = compare_branches(initial_branches, rerun_branches)

        self.assertEqual(1, len(notifications))
        self.assertEqual("jd", notifications[0].branch.project_name)
        self.assertEqual("feature/wut", notifications[0].branch.decoded_branch_name)
        self.assertEqual("#2", notifications[0].build.name)


if __name__ == '__main__':
    unittest.main()
