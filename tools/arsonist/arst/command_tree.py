from termcolor_util import green, blue, gray

from .file_resolver import FileResolver
from .project_reader import read_project_definition


def display_project_tree(projects_folder: str, project_name: str) -> None:
    project_definition = read_project_definition(
        projects_folder=projects_folder, project_name=project_name
    )
    file_resolver = project_definition.file_resolver()
    display_current_folder(file_resolver)


def display_current_folder(file_resolver: FileResolver, indent: int = 0) -> None:
    for entry in file_resolver.listdir():
        if entry.is_dir:
            print(
                "  " * indent
                + blue(entry.name, bold=True)
                + gray(f" ({entry.owning_project})", bold=True)
            )
            display_current_folder(file_resolver.subentry(entry), indent + 1)
        elif entry.is_exe:
            print(
                "  " * indent
                + green(entry.name, bold=True)
                + gray(f" ({entry.owning_project})", bold=True)
            )
        else:
            print(
                "  " * indent
                + entry.name
                + gray(f" ({entry.owning_project})", bold=True)
            )
