import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from .test_tasks import adhesive
from .check_equals import assert_equal_execution


class TestProcessExecutorSimple(unittest.TestCase):
    """
    Test if the process executor can execute simple processs.
    """
    def test_simple_execution(self):
        """
        Load a simple process and execute it.
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/adhesive.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Ensure Docker Tooling": 1,
            "Build Germanium Image": 1,
            "Test Chrome": 1,
            "Test Firefox": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

    """
    Test if the process executor can execute simple without waiting tasks.
    """
    def test_simple_execution_non_wait(self):
        """
        Load a simple process and execute it.
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/adhesive.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            "Ensure Docker Tooling": 1,
            "Build Germanium Image": 1,
            "Test Chrome": 1,
            "Test Firefox": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
