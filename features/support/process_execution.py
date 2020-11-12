import fcntl
import os
import subprocess
from typing import List


class ProcessExecution:
    def __init__(self, *, command: List[str]) -> None:
        self._process = subprocess.Popen(
            command, cwd=os.curdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    @property
    def stderr(self) -> str:
        """
        Reads the current content added to stderr in a nonblocking
        fashion
        """
        assert self._process.stderr

        fd = self._process.stderr
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        data = self._process.stderr.read()

        if not data:
            return ""

        return data.decode("utf-8")

    @property
    def stdout(self) -> str:
        """
        Reads the current content added to stdout in a nonblocking
        fashion.
        """
        assert self._process.stdout

        fd = self._process.stdout
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        data = self._process.stdout.read()

        if not data:
            return ""

        return data.decode("utf-8")

    def signal(self, sig) -> None:
        self._process.send_signal(sig)

    def kill(self) -> None:
        """
        Kills the current process
        """
        self._process.kill()
