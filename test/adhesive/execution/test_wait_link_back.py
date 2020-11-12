import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from .check_equals import assert_equal_execution
from .test_tasks import adhesive


class TestWaitLinkBack(unittest.TestCase):
    def test_link_back_execution(self):
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/link-back.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "Increment X by 1": 5,
            "Build Germanium Image": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
