from typing import List, Dict, Union
import mdvl
import sys
import os.path
import yaml
import pybars

from termcolor_util import red

from arst.file_resolver import FileResolver


class ParsedFile(object):
    name: str
    original_name: str
    keep_existing: bool
    hbs_template: bool

    def __init__(self, original_name: str) -> None:
        self.name = original_name
        self.original_name = original_name
        self.keep_existing = False
        self.hbs_template = False


class ProjectDefinition(object):
    name: str
    projects_folder: str
    search_path: List[str]
    generate_ars: bool
    shell_commands: List[str]

    def __init__(
        self, projects_folder: str, name: str, generate_ars: bool = True
    ) -> None:
        self.name = name
        self.projects_folder = projects_folder
        self.search_path = [name]
        self.generate_ars = generate_ars
        self.shell_commands: List[str] = []

    def file_resolver(self) -> FileResolver:
        return FileResolver(
            root_projects_folder=self.projects_folder, search_path=self.search_path
        )


def parse_file_name(
    file_name: str, project_parameters: Dict[str, Union[str, List[str]]]
) -> ParsedFile:
    """
    parseFileName - Parse the fie name
    :param file_name: string with filename
    :param project_parameters: the project parameters if they are used in the file name.
    :return: result dict
    """
    result = ParsedFile(file_name)

    name: str = file_name

    if name.endswith(".KEEP"):
        result.keep_existing = True
        name = name[0 : -len(".KEEP")]

    if name.endswith(".hbs"):
        result.hbs_template = True
        name = name[0 : -len(".hbs")]

    result.name = pybars.Compiler().compile(name)(project_parameters)

    return result


def read_project_definition(
    projects_folder: str, project_name: str
) -> ProjectDefinition:
    full_project_path = os.path.join(projects_folder, project_name)

    # Simple sanity check to see if there is a project there, instead
    # of reporting an error.
    if not os.path.isdir(full_project_path):
        print(
            red("Folder"),
            red(f"'{full_project_path}'", bold=True),
            red("does not exist, or is not a folder."),
        )
        sys.exit(1)

    help_file_name = os.path.join(projects_folder, project_name, "HELP.md")
    if os.path.isfile(help_file_name):
        with open(help_file_name, encoding="utf-8") as help_file:
            mdvl.render(help_file.read(), cols=80)

    result = ProjectDefinition(name=project_name, projects_folder=projects_folder)

    template_settings_path = os.path.join(full_project_path, ".ars")

    if not os.path.isfile(template_settings_path):
        return result

    with open(template_settings_path, encoding="utf-8") as template_settings_content:
        settings = yaml.safe_load(template_settings_content.read())

    if "noars" in settings and settings["noars"]:
        result.generate_ars = False

    if "parents" in settings:
        for parent in settings["parents"]:
            parent_project = read_project_definition(projects_folder, parent)
            result.search_path.extend(parent_project.search_path)
            result.shell_commands.extend(parent_project.shell_commands)

    if "commands" in settings:
        result.shell_commands.extend(settings["commands"])

    return result
