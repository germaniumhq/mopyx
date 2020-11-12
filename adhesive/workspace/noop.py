from contextlib import contextmanager
from typing import Optional, Union

from .Workspace import Workspace


class NoopWorkspace(Workspace):
    """
    A workspace that delegates everything to the parent workspace. This is
    used only to test various lifecycles in adhesive.
    """
    def __init__(self,
                 workspace: Workspace) -> None:
        super(NoopWorkspace, self).__init__(
            execution_id=workspace.execution_id,
            token_id=workspace.token_id,
            pwd=workspace.pwd)

        self.parent_workspace = workspace

    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:
        return self.parent_workspace.run(
            command,
            shell=shell,
            capture_stdout=capture_stdout,
        )

    def run_output(self,
                   command: str,
                   shell: str = "/bin/sh") -> str:
        return self.parent_workspace.run_output(command, shell=shell)

    def write_file(
            self,
            file_name: str,
            content: str) -> None:
        return self.parent_workspace.write_file(file_name, content)

    def rm(self, path: Optional[str]=None) -> None:
        self.parent_workspace.rm(path)

    def mkdir(self, path: str = None) -> None:
        self.parent_workspace.mkdir(path)

    def copy_to_agent(self,
                      from_path: str,
                      to_path: str):
        self.parent_workspace.copy_to_agent(from_path, to_path)

    def copy_from_agent(self,
                        from_path: str,
                        to_path: str):
        self.parent_workspace.copy_from_agent(from_path, to_path)

    def clone(self) -> 'NoopWorkspace':
        return NoopWorkspace(self.parent_workspace)


@contextmanager
def inside(workspace: Workspace):
    yield NoopWorkspace(workspace)
