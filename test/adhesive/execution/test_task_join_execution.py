import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from test.adhesive.execution.test_tasks import adhesive
from test.adhesive.execution.check_equals import assert_equal_execution


class TestTaskJoinExecution(unittest.TestCase):
    """
    Test if the process executor can process exclusive gateways.
    """
    def test_task_join_execution(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/task-join.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            'Build Germanium Image': 1,
            'Test Chrome': 1,
            'Test Firefox': 3,
        }, data.executions)

        self.assertFalse(process_executor.events,
                         "Some events were not unregistered and/or executed.")

    def test_task_join_execution_non_wait(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/task-join.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            'Build Germanium Image': 3,  # 1 chrome + 2 firefox
            'Test Chrome': 1,
            'Test Firefox': 3,
        }, data.executions)

        self.assertFalse(process_executor.events,
                         "Some events were not unregistered and/or executed.")


if __name__ == '__main__':
    unittest.main()
