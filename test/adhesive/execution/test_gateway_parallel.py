import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from .test_tasks import adhesive
from .check_equals import assert_equal_execution


class TestGatewayParallel(unittest.TestCase):
    """
    Test if the process executor can process parallel gateways.
    """
    def test_parallel_gateway(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-parallel.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Test Chrome": 3,
            "Build Germanium Image": 3,
        }, data.executions)
        self.assertFalse(process_executor.events)

    def test_parallel_gateway_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/gateway-parallel.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Test Chrome": 3,
            "Build Germanium Image": 3,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
