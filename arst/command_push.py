import os.path
import pathlib
import shutil
from typing import List

from termcolor_util import yellow


def push_files_to_template(
    projects_folder: str, project_name: str, files_to_push: List[str]
) -> None:
    for file_name in files_to_push:
        recursively_push_file(projects_folder, project_name, file_name)


def recursively_push_file(
    projects_folder: str, project_name: str, file_name: str
) -> None:
    print(
        yellow("Pushing"),
        yellow(file_name, bold=True),
        yellow("to"),
        yellow(project_name, bold=True),
    )

    target_file_name = os.path.join(projects_folder, project_name, file_name)
    if os.path.isdir(file_name):
        pathlib.Path(target_file_name).mkdir(parents=True, exist_ok=True)
        for nested_file_name in os.listdir(file_name):
            recursively_push_file(
                projects_folder=projects_folder,
                project_name=project_name,
                file_name=os.path.join(file_name, nested_file_name),
            )
        return

    pathlib.Path(target_file_name).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(file_name, target_file_name)
