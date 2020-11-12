import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from test.adhesive.execution.check_equals import assert_equal_execution
from .test_tasks import adhesive


class TestProcessExecutorSubProcess(unittest.TestCase):
    def test_sub_process_execution(self):
        """
        Load a process that contains a sub process and execute it.
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/adhesive_subprocess.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            'Ensure Docker Tooling': 1,
            'Build Germanium Image': 1,
            'Prepare Firefox': 1,
            'Test Firefox': 1,
            'Test Chrome': 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

    def test_sub_process_execution_non_wait(self):
        """
        Load a process that contains a sub process and execute it.
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/adhesive_subprocess.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            'Ensure Docker Tooling': 1,
            'Build Germanium Image': 1,
            'Prepare Firefox': 1,
            'Test Firefox': 1,
            'Test Chrome': 1,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
