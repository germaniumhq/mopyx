import os
import uuid
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional, Union


class Workspace(ABC):
    """
    A workspace is a place where work can be done. That means a writable
    folder is being allocated, that will be cleaned up at the end of the
    execution.

    :param execution_id: The execution id of the whole process.
    :param token_id: The id of the current token being processed.
    :param pwd: The current folder.
    """
    def __init__(self,
                 execution_id: str,
                 token_id: str,
                 pwd: str) -> None:
        self.execution_id = execution_id
        self.token_id = token_id
        self.pwd = pwd

    @abstractmethod
    def write_file(
            self,
            file_name: str,
            content: str) -> None:
        pass

    # FIXME: split this into two methods, instead of the `capture_stdout` flag
    @abstractmethod
    def run(self,
            command: str,
            shell: str = "/bin/sh",
            capture_stdout: bool = False) -> Union[str, None]:
        """
        Run a new command in the current workspace.

        :param capture_stdout:
        :param command:
        :return:
        """
        pass

    @abstractmethod
    def run_output(self,
            command: str,
            shell: str = "/bin/sh") -> str:
        """
        Run a new command in the current workspace, and returns the stdout as a string.
        If the command returns a non-zero exit code, an exception is thrown.

        :param capture_stdout:
        :param command:
        :return:
        """
        pass

    @abstractmethod
    def rm(self, path: Optional[str] = None) -> None:
        """
        Recursively remove the file or folder given as path. If no path is sent,
        the whole `pwd` will be cleared.

        :param path:
        :return:
        """
        pass

    @abstractmethod
    def mkdir(self, path: Optional[str] = None) -> None:
        """
        Create a folder, including all its needed parents. If no path is sent,
        the current `pwd` will be used.

        :param path:
        :return:
        """
        pass

    @abstractmethod
    def copy_to_agent(self,
                      from_path: str,
                      to_path: str) -> None:
        """
        Copy the files to the agent from the current disk.
        :param from_path:
        :param to_path:
        :return:
        """
        pass

    @abstractmethod
    def copy_from_agent(self,
                        from_path: str,
                        to_path: str) -> None:
        """
        Copy the files from the agent to the current disk.
        :param from_path:
        :param to_path:
        :return:
        """
        pass

    @contextmanager
    def temp_folder(self):
        """
        Create a temporary folder in the current `pwd` that will be deleted
        when the `with` block ends.

        :return:
        """
        current_folder = self.pwd
        folder = os.path.join(self.pwd, str(uuid.uuid4()))

        self.mkdir(folder)
        self.pwd = folder

        try:
            yield folder
        finally:
            self.rm(folder)
            self.pwd = current_folder

    @contextmanager
    def chdir(self, target_folder: str):
        """
        Temporarily change a folder, that will go back to the original `pwd`
        when the `with` block ends. To change the folder for the workspace
        permanently, simply assing the `pwd`.
        :param target_folder:
        :return:
        """
        current_folder = self.pwd
        folder = os.path.join(self.pwd, target_folder)

        self.pwd = folder

        try:
            yield folder
        finally:
            self.pwd = current_folder

    @abstractmethod
    def clone(self) -> 'Workspace':
        """
        Clone the current workspace, so parallel tasks can do
        things such as chdir, or temp_folder.
        :return:
        """
        pass

    @property
    def id(self) -> str:
        return f"{self.execution_id}:{self.token_id}"
