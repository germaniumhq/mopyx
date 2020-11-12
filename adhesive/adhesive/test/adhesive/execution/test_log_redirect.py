import glob
import os
import unittest

from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive import logredirect
from adhesive.process_read.bpmn import read_bpmn_file
import adhesive.config as config
from test.adhesive.execution.check_equals import assert_equal_execution
from test.adhesive.execution.test_tasks import adhesive


class TestIfLogRedirectionWorks(unittest.TestCase):
    """
    Test if the process executor can process inclusive gateways.
    """
    def test_log_redirection(self):
        """
        Load a process with a gateway and test it..
        """
        adhesive.process.process = read_bpmn_file("test/adhesive/xml/redirect-logs.bpmn")

        process_executor = ProcessExecutor(adhesive.process)
        data = process_executor.execute()

        assert_equal_execution({
            "sh: echo hello world && echo bad world >&2 && echo good world": 1,
            "Store current execution id": 1,
        }, data.executions)
        self.assertFalse(process_executor.events)

        adhesive_temp_folder = config.current.temp_folder
        path_to_glob = os.path.join(adhesive_temp_folder, data.execution_id, "logs", "_4", "*", "stdout")

        log_path = glob.glob(path_to_glob)

        if not log_path:
            raise Exception(f"Unable to match any file for glob {path_to_glob}")

        with open(log_path[0], "rt") as f:
            self.assertEqual(f.read(), "sh: echo hello world && "
                                       "echo bad world >&2 && "
                                       "echo good world\nhello world\ngood world\n")

        log_path = glob.glob(os.path.join(
            adhesive_temp_folder,
            data.execution_id,
            "logs",
            "_4",
            "*",
            "stderr"))

        with open(log_path[0], "rt") as f:
            self.assertEqual(f.read(), "bad world\n")


if __name__ == '__main__':
    unittest.main()

