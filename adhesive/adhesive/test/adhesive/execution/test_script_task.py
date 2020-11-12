import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file

from .test_tasks import adhesive
from .check_equals import assert_equal_execution


class TestScriptTask(unittest.TestCase):
    """
    Test if the process executor can process script tasks.
    """
    def test_script_task_execution(self):
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/script.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            'Script Task': 1,
            'Build Germanium Image': 1,
        }, data.executions)

        self.assertFalse(process_executor.events,
                         "Some events were not unregistered and/or executed.")
