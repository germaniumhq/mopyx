import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from test.adhesive.execution.check_equals import assert_equal_execution

from .test_tasks import adhesive


class TestGatewayExecution(unittest.TestCase):
    """
    Test if the process executor can process exclusive gateways.
    """
    def test_exclusive_gateway(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/exclusive_gateway.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Populate task data": 1,
            "Exclusive default branch": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

    def test_exclusive_gateway_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/exclusive_gateway.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            "Populate task data": 1,
            "Exclusive default branch": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

if __name__ == '__main__':
    unittest.main()
