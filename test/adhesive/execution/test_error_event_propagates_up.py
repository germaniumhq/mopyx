import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from test.adhesive.execution.test_tasks import adhesive
from test.adhesive.execution.check_equals import assert_equal_execution


class TestErrorEventPropagatesUp(unittest.TestCase):
    """
    Test if the process executor can process parallel gateways.
    """
    def test_error_propagates_up(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/error-event-subprocess-propagates-up.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Error Was Caught": 1,
        }, data.executions)

        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
