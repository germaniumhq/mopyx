import os
import shlex
import sys
from contextlib import contextmanager
from typing import Optional, Union, Iterable, Generator
from uuid import uuid4
import logging

from adhesive.storage.task_storage import get_folder
from .Workspace import Workspace

LOG = logging.getLogger(__name__)


class DockerWorkspace(Workspace):
    def __init__(self,
                 workspace: Workspace,
                 image_name: str,
                 extra_docker_params: str = "",
                 pwd: Optional[str] = None,
                 container_id: Optional[str] = None) -> None:
        super(DockerWorkspace, self).__init__(
            execution_id=workspace.execution_id,
            token_id=workspace.token_id,
            pwd=pwd if pwd else workspace.pwd)

        self.parent_workspace = workspace
        self.image = image_name

        if container_id is not None:
            self.container_id = container_id
            return

        pwd = workspace.pwd

        uid = workspace.run_output("id -u").strip()
        gid = workspace.run_output("id -g").strip()
        groups = workspace.run_output("id -G").strip().split(" ")

        if groups:
            groups_str = ""
            for group in groups:
                groups_str += f"--group-add {group} "
        else:
            groups_str = ""

        command = "docker run -t "

        if pwd and pwd != "/":
            command += f"-v {pwd}:{pwd} "

        command += "-d "
        command += "--entrypoint cat "
        command += f"-u {uid}:{gid} "
        command += f"{groups_str} "
        command += f"{extra_docker_params} "
        command += f"{shlex.quote(image_name)}"

        self.container_id = workspace.run_output(command).strip()

    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:

        LOG.debug(f"Workspace: docker({self.id}).run: {command}")

        return self.parent_workspace.run(
                f"docker exec -w {shlex.quote(self.pwd)} {shlex.quote(self.container_id)} {shell} -c {shlex.quote(command)}",
                capture_stdout=capture_stdout)

    def run_output(self,
                   command: str,
                   shell: str = "/bin/sh") -> str:

        LOG.debug(f"Workspace: docker({self.id}).run: {command}")

        return self.parent_workspace.run_output(
                f"docker exec -w {shlex.quote(self.pwd)} {shlex.quote(self.container_id)} {shell} -c {shlex.quote(command)}")

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
        if path is None:
            full_path = self.pwd
        else:
            full_path = os.path.join(self.pwd, path)

        self.run(f"mkdir -p {shlex.quote(full_path)}")

    def copy_to_agent(self,
                      from_path: str,
                      to_path: str):
        self.parent_workspace.run(
                f"docker cp {from_path} {self.container_id}:{to_path}")

    def copy_from_agent(self,
                        from_path: str,
                        to_path: str):
        self.parent_workspace.run(
                f"docker cp {self.container_id}:{from_path} {to_path}")

    def clone(self) -> 'DockerWorkspace':
        # FIXME: should return the parent workspace somehow
        return DockerWorkspace(
            workspace=self.parent_workspace,
            image_name=self.image,
            pwd=self.pwd,
            container_id=self.container_id,
        )

    def _destroy(self):
        self.parent_workspace.run(
                f"docker rm -f {self.container_id}")


@contextmanager
def inside(workspace: Workspace,
           image_name: str,
           extra_docker_params: str = ""):
    w = None

    try:
        w = DockerWorkspace(workspace=workspace,
                            image_name=image_name,
                            extra_docker_params=extra_docker_params)
        yield w
    finally:
        if w is not None:
            w._destroy()


def build(workspace: Workspace,
          tags: Union[str, Iterable[str]]) -> str:

    # we always consider a list of tags
    if isinstance(tags, str):
        tags = [tags]

    command = "docker build "

    for tag in tags:
        command += f"-t {tag} -q "

    command += "."

    return workspace.run_output(command)
