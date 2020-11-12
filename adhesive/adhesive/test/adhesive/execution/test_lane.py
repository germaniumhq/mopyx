import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from test.adhesive.execution.test_tasks import adhesive
from test.adhesive.execution.check_equals import assert_equal_execution


class TestLane(unittest.TestCase):
    """
    Test if the process executor can process parallel gateways.
    """
    def test_lane(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/lane.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Prepare Firefox": 1,
            "Test Chrome": 1,
            "Test Firefox": 1,
            "Ensure Docker Tooling": 1,
            "Build Germanium Image": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

    def test_lane_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/lane.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            "Prepare Firefox": 1,
            "Test Chrome": 1,
            "Test Firefox": 2,
            "Ensure Docker Tooling": 1,
            "Build Germanium Image": 4,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
