import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from test.adhesive.execution.ui_provider import TestUserTaskProvider
from test.adhesive.execution.test_tasks import adhesive


class TestUserTaskBasic(unittest.TestCase):
    def test_link_back_execution(self):
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/user-task.bpmn")

        process_executor = ProcessExecutor(adhesive.process,
                                             ut_provider=TestUserTaskProvider())
        data = process_executor.execute()

        self.assertEqual("OK", data.OK)
        self.assertEqual("Cancel", data.Cancel)
        self.assertEqual("branch", data.branch)
        self.assertEqual("12.0", data.version)
        self.assertEqual("password", data.password)
        self.assertEqual(('integration',), data.run_tests)

        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
