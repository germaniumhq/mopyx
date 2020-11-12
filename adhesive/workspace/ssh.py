from typing import Union, Optional, Any, Dict
import shlex
from contextlib import contextmanager
import paramiko
import sys
import os
import logging

from adhesive.workspace.Workspace import Workspace

LOG = logging.getLogger(__name__)


class SshWorkspace(Workspace):
    def __init__(self,
                 execution_id: str,
                 token_id: str,
                 ssh: str,
                 pwd: Optional[str] = None,
                 ssh_connection=None,
                 **kw: Dict[str, Any]) -> None:
        super(SshWorkspace, self).__init__(
            execution_id=execution_id,
            token_id=token_id,
            pwd='/' if not pwd else pwd)

        # cloning needs to create new connections since tasks are executed
        # in different processes
        self._ssh = ssh
        self._kw = kw

        if ssh_connection:
            self.ssh = ssh_connection
        else:
            self.ssh = paramiko.client.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            self.ssh.connect(ssh, **kw)

        self._sftp = None

    @property
    def sftp(self):
        if not self._sftp:
            self._sftp = self.ssh.open_sftp()

        return self._sftp

    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:

        channel = None

        try:
            parsed_command = f"cd {shlex.quote(self.pwd)};{command}"
            shell_command = f"{shell} -c {shlex.quote(parsed_command)}"

            LOG.debug(f"Workspace: ssh({self.id}).run: {shell_command}")

            stdin, stdout, stderr = self.ssh.exec_command(shell_command)
            channel = stdout.channel

            if capture_stdout:
                result = bytes()

                while not channel.exit_status_ready() or channel.recv_ready() or channel.recv_stderr_ready():
                    while channel.recv_ready():
                        result += channel.recv(1024)

                    while channel.recv_stderr_ready():
                        os.write(sys.stderr.fileno(), channel.recv_stderr(1024))

                exit_status = channel.recv_exit_status()

                if exit_status != 0:
                    raise Exception(f"Exit status is not zero, instead is {exit_status}")

                return result.decode('utf-8')

            while not channel.exit_status_ready() or channel.recv_ready() or channel.recv_stderr_ready():
                while channel.recv_ready():
                    os.write(sys.stdout.fileno(), channel.recv(1024))

                while channel.recv_stderr_ready():
                    os.write(sys.stderr.fileno(), channel.recv_stderr(1024))

            exit_status = channel.recv_exit_status()

            if exit_status != 0:
                raise Exception(f"Exit status is not zero, instead is {exit_status}")
        finally:
            if channel:
                channel.close()

        return None

    def run_output(self,
                   command: str,
                   shell: str = "/bin/sh") -> str:

        channel = None

        try:
            parsed_command = f"cd {shlex.quote(self.pwd)};{command}"
            shell_command = f"{shell} -c {shlex.quote(parsed_command)}"

            LOG.debug(f"Workspace: ssh({self.id}).run: {shell_command}")

            stdin, stdout, stderr = self.ssh.exec_command(shell_command)
            channel = stdout.channel

            result = bytes()

            while not channel.exit_status_ready() or channel.recv_ready() or channel.recv_stderr_ready():
                while channel.recv_ready():
                    result += channel.recv(1024)

                while channel.recv_stderr_ready():
                    os.write(sys.stderr.fileno(), channel.recv_stderr(1024))

            exit_status = channel.recv_exit_status()

            if exit_status != 0:
                raise Exception(f"Exit status is not zero, instead is {exit_status}")

            return result.decode('utf-8')
        finally:
            if channel:
                channel.close()

        return None

    def write_file(
            self,
            file_name: str,
            content: str) -> None:
        self.sftp.chdir(self.pwd)
        with self.sftp.file(file_name, "w") as f:
            f.write(content)

    def rm(self, path: Optional[str] = None) -> None:
        if path is None:
            self.run(f'rm -fr {shlex.quote(self.pwd)}')
            return

        self.run(f'rm -fr {shlex.quote(path)}')

    def mkdir(self, path: Optional[str] = None) -> None:
        if path is None:
            self.run(f'mkdir -p {shlex.quote(self.pwd)}')
            return

        self.run(f'mkdir -p {shlex.quote(path)}')

    def copy_to_agent(self,
                      from_path: str,
                      to_path: str):
        raise Exception("not implemented")

    def copy_from_agent(self,
                        from_path: str,
                        to_path: str):
        raise Exception("not implemented")

    def clone(self) -> 'SshWorkspace':
        result = SshWorkspace(execution_id=self.execution_id,
                              token_id=self.token_id,
                              ssh=self._ssh,
                              pwd=self.pwd,
                              ssh_connection=self.ssh)

        return result

    def _destroy(self) -> None:
        if self._sftp:
            self._sftp.close()
        self.ssh.close()

# TypeError: Can't instantiate abstract class SshWorkspace with abstract
# methods clone, copy_from_agent, copy_to_agent, mkdir, rm, write_file


@contextmanager
def inside(workspace: Workspace,
           ssh: str,
           **kw):
    w = None

    try:
        w = SshWorkspace(execution_id=workspace.execution_id,
                         token_id=workspace.token_id,
                         ssh=ssh,
                         **kw)
        yield w
    finally:
        if w is not None:
            w._destroy()
