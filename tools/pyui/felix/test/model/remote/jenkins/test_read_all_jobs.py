import unittest

from .test_jenkins_build_loading import load_result

from germanium_build_monitor.model.jenkins.remote.read_job_tree import process
from germanium_build_monitor.model.JenkinsFolder import JenkinsFolder


class TestAllJobsReading(unittest.TestCase):
    """
    Attempt at reading the jobs from the Jenkins json
    """

    def test_read_all_jobs(self) -> None:
        """
        Read dem data.
        """
        result = load_result("all_jobs.json")
        root = JenkinsFolder(None, "__root__")

        process(root, result)

        self.assertEqual(3, len(root.jobs))


if __name__ == '__main__':
    unittest.main()
