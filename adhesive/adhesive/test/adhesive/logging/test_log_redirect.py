import sys
import unittest
import uuid

from adhesive.logredirect.LogRedirect import redirect_stdout
from adhesive import logredirect
from adhesive.storage.task_storage import ensure_folder

import threading


class TestLogRedirection(unittest.TestCase):
    def test_file_redirection_logs(self):
        original_stdout_fileno = sys.stdout.fileno()
        original_stderr_fileno = sys.stderr.fileno()

        target_folder = ensure_folder(str(uuid.uuid4()))

        print("x")
        self.assertEqual(original_stdout_fileno, sys.stdout.fileno())
        self.assertEqual(original_stderr_fileno, sys.stderr.fileno())

        print(sys.stdout)

        with redirect_stdout(target_folder):
            print("y")
            self.assertNotEqual(original_stdout_fileno, sys.stdout.fileno())
            self.assertNotEqual(original_stderr_fileno, sys.stderr.fileno())

        print("z")
        self.assertEqual(original_stdout_fileno, sys.stdout.fileno())
        self.assertEqual(original_stderr_fileno, sys.stderr.fileno())


if __name__ == '__main__':
    unittest.main()
