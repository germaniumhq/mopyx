import logging
import os
import shutil
import subprocess
import sys
from distutils.dir_util import copy_tree
from typing import Optional, Union

from adhesive.workspace.Workspace import Workspace

LOG = logging.getLogger(__name__)


class LocalLinuxWorkspace(Workspace):
    """
    A workspace is a place where work can be done. That means a writable
    folder is being allocated, that will be cleaned up at the end of the
    execution.
    """
    def __init__(self,
                 execution_id: str,
                 token_id: str,
                 pwd: str="") -> None:
        super(LocalLinuxWorkspace, self).__init__(
            execution_id=execution_id,
            token_id=token_id,
            pwd=pwd,
        )

        if not pwd:
            self.pwd = ensure_folder(self)

    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:
        if capture_stdout:
            return subprocess.check_output(
                [
                    shell, "-c", command
                ],
                cwd=self.pwd,
                stderr=sys.stderr,
            ).decode('utf-8')

        subprocess.check_call(
            [
                shell, "-c", command
            ],
            cwd=self.pwd,
            stdout=sys.stdout,
            stderr=sys.stderr)

        return None

    def run_output(self,
                   command: str,
                   shell: str = "/bin/sh") -> str:
        return subprocess.check_output(
            [
                shell, "-c", command
            ],
            cwd=self.pwd,
            stderr=sys.stderr,
        ).decode('utf-8')

    def write_file(
            self,
            file_name: str,
            content: str) -> None:

        full_path = os.path.join(self.pwd, file_name)

        with open(full_path, "wt") as f:
            f.write(content)

    def rm(self, path: Optional[str]=None) -> None:
        if path is None:
            LOG.debug("rmtree {}", self.pwd)
            shutil.rmtree(self.pwd)
            return

        if not path:
            raise Exception("You need to pass a subpath to delete")

        remove_path = os.path.join(self.pwd, path)

        LOG.debug("rmtree {}", remove_path)

        if os.path.isfile(remove_path):
            os.remove(remove_path)
        else:
            shutil.rmtree(remove_path)

    def mkdir(self, path: str=None) -> None:
        LOG.debug("mkdir {}", path)

        full_path = self.pwd

        if path is not None:
            full_path = os.path.join(self.pwd, path)

        if os.path.isdir(full_path):
            return

        os.mkdir(full_path)

    def copy_to_agent(self,
                      from_path: str,
                      to_path: str):
        LOG.debug("copy {} to {}", from_path, to_path)
        copy_tree(from_path, to_path)

    def copy_from_agent(self,
                        from_path: str,
                        to_path: str):
        LOG.debug("copy {} to {}", from_path, to_path)
        shutil.copytree(from_path, to_path)

    def clone(self) -> 'LocalLinuxWorkspace':
        return LocalLinuxWorkspace(
            execution_id=self.execution_id,
            token_id=self.token_id,
            pwd=self.pwd,
        )


from adhesive.storage.task_storage import ensure_folder

