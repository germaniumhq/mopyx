import logging
import os
import shlex
from contextlib import contextmanager
from typing import Optional, Union
from uuid import uuid4

from adhesive.storage.task_storage import get_folder
from adhesive.workspace.Workspace import Workspace

LOG = logging.getLogger(__name__)


class KubeWorkspace(Workspace):
    def __init__(self,
                 workspace: Workspace,
                 pwd: Optional[str] = None,
                 pod_name: Optional[str] = None,
                 namespace: Optional[str] = None) -> None:
        super(KubeWorkspace, self).__init__(
            execution_id=workspace.execution_id,
            token_id=workspace.token_id,
            pwd=pwd if pwd else workspace.pwd)

        self.parent_workspace = workspace

        if pod_name is None:
            raise Exception("You need to pass the pod name")

        assert pod_name

        self.pod_name: str = pod_name
        self.namespace = namespace

    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:

        LOG.debug(f"Workspace: kube({self.id}).run: {command}")
        parsed_command = f"cd {shlex.quote(self.pwd)};{command}"

        exec_command = f"kubectl exec {shlex.quote(self.pod_name)} "

        if self.namespace:
            exec_command += f"--namespace {shlex.quote(self.namespace)} "

        exec_command += f"-- {shell} -c {shlex.quote(parsed_command)}"

        return self.parent_workspace.run(exec_command, capture_stdout=capture_stdout)

    def run_output(self,
                   command: str,
                   shell: str = "/bin/sh") -> str:
        LOG.debug(f"Workspace: kube({self.id}).run: {command}")
        parsed_command = f"cd {shlex.quote(self.pwd)};{command}"

        exec_command = f"kubectl exec {shlex.quote(self.pod_name)} "

        if self.namespace:
            exec_command += f"--namespace {shlex.quote(self.namespace)} "

        exec_command += f"-- {shell} -c {shlex.quote(parsed_command)}"

        return self.parent_workspace.run_output(exec_command)

    def write_file(
            self,
            file_name: str,
            content: str) -> None:
        """
        Write a file on the remote docker instance. Since we can't
        really just write files, we create a temp file, then we
        copy it remotely.
        :param file_name:
        :param content:
        :return:
        """
        try:
            self.parent_workspace.mkdir(get_folder(self))
            tmp_file = os.path.join(get_folder(self), str(uuid4()))
            self.parent_workspace.write_file(tmp_file, content)
            self.copy_to_agent(tmp_file, file_name)
        finally:
            self.parent_workspace.rm(tmp_file)

    def rm(self, path: Optional[str]=None) -> None:
        """
        Remove a path from the container. We're calling `rm` to do
        the actual operation.
        :param path:
        :return:
        """
        if not path:
            raise Exception("You need to pass a subpath for deletion")

        self.run(f"rm -fr {shlex.quote(path)}")

    def mkdir(self, path: str = None) -> None:
        if path is not None:
            full_path = os.path.join(self.pwd, path)
        else:
            full_path = self.pwd

        self.run(f"mkdir -p {shlex.quote(full_path)}")

    def copy_to_agent(self,
                      from_path: str,
                      to_path: str):
        if self.namespace is not None:
            self.parent_workspace.run(
                f"kubectl cp --namespace {shlex.quote(self.namespace)} "
                f"{from_path} {self.pod_name}:{to_path}")
            return

        self.parent_workspace.run(
                f"kubectl cp {from_path} {self.pod_name}:{to_path}")

    def copy_from_agent(self,
                        from_path: str,
                        to_path: str):
        if self.namespace is not None:
            self.parent_workspace.run(
                    f"kubectl cp --namespace {shlex.quote(self.namespace)} "
                    f"{self.pod_name}:{from_path} {to_path}")

        self.parent_workspace.run(f"kubectl cp {self.pod_name}:{from_path} {to_path}")

    def clone(self) -> 'KubeWorkspace':
        # FIXME: should return the parent workspace somehow
        return KubeWorkspace(
            workspace=self.parent_workspace,
            pod_name=self.pod_name,
            pwd=self.pwd,
            namespace=self.namespace,
        )

    def _destroy(self):
        self.parent_workspace.run(
                f"kubectl rm "
                f"--namespace {shlex.quote(self.namespace)} "
                f"-f {self.pod_name}")


@contextmanager
def inside(workspace: Workspace,
           pod_name: str,
           namespace: Optional[str] = None):
    try:
        w = KubeWorkspace(workspace=workspace,
                          pod_name=pod_name,
                          pwd="/",
                          namespace=namespace)
        yield w
    finally:
        pass
