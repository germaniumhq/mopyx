import unittest

import adhesive.logging
from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.process_read.bpmn import read_bpmn_file
from test.adhesive.execution.check_equals import assert_equal_execution
from test.adhesive.execution.test_tasks import adhesive

adhesive.config.current = adhesive.config.LocalConfigReader.read_configuration()
adhesive.logging.configure_logging(adhesive.config.current)


class TestLoopExecution(unittest.TestCase):

    def test_loop_execution(self):
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/loop.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            'Build Germanium Image on mac': 1,
            'Build Germanium Image on windows': 1,
            'Build Germanium Image on linux': 1,
            'Test Browser ie on linux': 1,
            'Cleanup Platform linux': 1,
            'Cleanup Platform windows': 1,
            'Cleanup Platform mac': 1,
            'Test Browser chrome on linux': 1,
            'Test Browser edge on linux': 1,
            'Test Browser edge on windows': 1,
            'Test Browser chrome on windows': 1,
            'Test Browser ie on windows': 1,
            'Test Browser chrome on mac': 1,
            'Test Browser edge on mac': 1,
            'Test Browser ie on mac': 1,
        }, data.executions)

        self.assertFalse(process_executor.events)

    def test_loop_execution_no_wait(self):
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/loop.bpmn")

        process_executor = ProcessExecutor(adhesive.process, wait_tasks=False)
        data = process_executor.execute()

        assert_equal_execution({
            'Build Germanium Image on mac': 1,
            'Build Germanium Image on windows': 1,
            'Build Germanium Image on linux': 1,
            'Test Browser ie on linux': 1,
            'Cleanup Platform linux': 3,
            'Cleanup Platform windows': 3,
            'Cleanup Platform mac': 3,
            'Test Browser chrome on linux': 1,
            'Test Browser edge on linux': 1,
            'Test Browser edge on windows': 1,
            'Test Browser chrome on windows': 1,
            'Test Browser ie on windows': 1,
            'Test Browser chrome on mac': 1,
            'Test Browser edge on mac': 1,
            'Test Browser ie on mac': 1,
        }, data.executions)

        self.assertFalse(process_executor.events)


if __name__ == '__main__':
    unittest.main()
