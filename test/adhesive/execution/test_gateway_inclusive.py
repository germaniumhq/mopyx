import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from .test_tasks import adhesive
from .check_equals import assert_equal_execution


class TestInclusiveGateway(unittest.TestCase):
    """
    Test if the process executor can process inclusive gateways.
    """
    def test_inclusive_gateway(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-inclusive.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Test Chrome": 1,
            "Test Firefox": 1,
            "Build Germanium Image": 1,
            "Cleanup Broken Tasks": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

    def test_inclusive_gateway_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-inclusive.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            "Test Chrome": 1,
            "Test Firefox": 1,
            "Build Germanium Image": 1,
            "Cleanup Broken Tasks": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
