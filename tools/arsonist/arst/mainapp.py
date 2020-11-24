from typing import Callable, TypeVar, Union, List, cast

import functools
import click
import filecmp
import yaml
import os
import shutil
import sys
import pybars
import colorama
import subprocess
import re
from typing import Dict, Optional
from textwrap import dedent
import datetime
import time
from termcolor_util import cyan, red, yellow

from arst.file_resolver import FileResolver, is_first_file_newer
from arst.project_reader import (
    ProjectDefinition,
    read_project_definition,
    ParsedFile,
    parse_file_name,
)

from arst.command_push import push_files_to_template
from arst.command_tree import display_project_tree
from arst.command_ls import list_project_folder
from arst.command_lls import list_folder_in_project
from arst.command_pwd import display_project_location
from arst.command_edit import edit_file_from_project
from arst.command_diff import diff_file_from_project

T = TypeVar("T")


ARS_PROJECTS_FOLDER: str = (
    os.environ["ARS_PROJECTS_FOLDER"]
    if "ARS_PROJECTS_FOLDER" in os.environ
    else os.path.join(os.environ["HOME"], ".projects")
)

ARS_DIFF_TOOL: str = (
    os.environ["ARS_DIFF_TOOL"]
    if "ARS_DIFF_TOOL" in os.environ
    else os.path.join("vimdiff")
)


PARAM_RE = re.compile("^(.*?)(=(.*))?$")


def now() -> float:
    return time.mktime(datetime.datetime.now().timetuple())


def execute_diff(file1: str, file2: str) -> None:
    """
    Run an external diff program on the two files
    """
    subprocess.call([ARS_DIFF_TOOL, file1, file2])


def coloramafn(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        try:
            colorama.init()
            return f(*args, **kw)
        finally:
            colorama.deinit()

    return wrapper


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        generate()


@main.command()
@coloramafn
def version():
    """
    Print the current application version
    """
    print(
        cyan(
            dedent(
                r"""\
                                _     _
      __ _ _ __ ___  ___  _ __ (_)___| |_
     / _` | '__/ __|/ _ \| '_ \| / __| __|
    | (_| | |  \__ \ (_) | | | | \__ \ |_
     \__,_|_|  |___/\___/|_| |_|_|___/\__|
                           version: 0.1.master
    """
            ),
            bold=True,
        )
    )
    sys.exit(0)


@main.command()
@click.option("--project", required=False)
@click.argument("files_to_push", nargs=-1)
@coloramafn
def push(*, project, files_to_push):
    """
    Push a file into the template. If a template is not passed, the first template
    is used.
    """
    if not project:
        project_parameters = load_project_parameters()

        if not project_parameters:
            print(
                red("Not in a project."), red(".ars", bold=True), red("file not found.")
            )
            sys.exit(1)

        project = project_parameters["templates"][0]

    push_files_to_template(ARS_PROJECTS_FOLDER, project, files_to_push)


@main.command()
@click.argument("project_name")
@coloramafn
def tree(project_name):
    """
    Display the project tree
    """
    display_project_tree(ARS_PROJECTS_FOLDER, project_name)


@main.command()
@click.argument("project_folder", required=False)
@coloramafn
def ls(project_folder):
    """
    List the project folder
    """
    list_project_folder(ARS_PROJECTS_FOLDER, project_folder)


@main.command()
@click.argument("project_name")
@coloramafn
def pwd(project_name):
    """
    Display the project location
    """
    display_project_location(ARS_PROJECTS_FOLDER, project_name)


@main.command()
@click.option("--project", required=False)
@click.argument("file_to_edit")
@coloramafn
def edit(project: Optional[str], file_to_edit: str) -> None:
    """
    Edit a file from the project. If a template is not used, the first
    template from the project is used.
    """
    project_parameters = load_project_parameters()

    if not project_parameters:
        print(red("Not in a project."), red(".ars", bold=True), red("file not found."))
        sys.exit(1)

    if not project:
        project = project_parameters["templates"][0]

    edit_file_from_project(
        ARS_PROJECTS_FOLDER, project, file_to_edit, load_project_parameters()
    )


@main.command()
@click.argument("file_to_diff")
@coloramafn
def diff(file_to_diff: str) -> None:
    """
    Diff a file against the template. If a project is not sent,
    the first template is being used.
    """
    project_parameters = load_project_parameters()

    if not project_parameters:
        print(red("Not in a project."), red(".ars", bold=True), red("file not found."))
        sys.exit(1)

    diff_file_from_project(
        ARS_PROJECTS_FOLDER,
        cast(List[str], project_parameters["templates"]),
        file_to_diff,
        project_parameters,
    )


@main.command()
@click.argument("folder_to_list", default=".")
@coloramafn
def lls(folder_to_list: str) -> None:
    """
    List a folder from the project
    """
    list_folder_in_project(
        ARS_PROJECTS_FOLDER, folder_to_list, load_project_parameters()
    )


def load_project_parameters() -> Optional[Dict[str, Union[str, List[str]]]]:
    loaded_project_parameters: Optional[Dict[str, Union[str, List[str]]]] = None

    if os.path.isfile(".ars"):
        with open(".ars", "r", encoding="utf8") as f:
            loaded_project_parameters = yaml.safe_load(f)
            print(
                cyan("Using already existing"),
                cyan("'.ars'", bold=True),
                cyan("file settings:"),
                cyan(str(loaded_project_parameters), bold=True),
            )

    return loaded_project_parameters


@main.command()
@click.option("--ars/--no-ars", default=True)
@click.option("--auto", required=False)
@click.option("--keep", required=False)
@click.argument("template", required=False)
@click.argument("parameters", nargs=-1)
@coloramafn
def generate(ars, auto, keep, template, parameters):
    """
    Generate or update the project sources
    """
    loaded_project_parameters = load_project_parameters()

    if not template and not loaded_project_parameters:
        print(red("You need to pass a project name to generate."))

        if os.path.isdir(ARS_PROJECTS_FOLDER):
            print("Available projects (%s):" % cyan(ARS_PROJECTS_FOLDER))
            list_project_folder(ARS_PROJECTS_FOLDER, None)
        else:
            print(f"{ARS_PROJECTS_FOLDER} folder doesn't exist.")

        sys.exit(1)

    # if we have arguments, we need to either create, or augument the projectParameters
    # with the new settings.
    project_parameters = (
        loaded_project_parameters if loaded_project_parameters else dict()
    )

    # we convert the old projects into the new format.
    if "NAME" in project_parameters:
        project_parameters["templates"] = [project_parameters["NAME"]]
        del project_parameters["NAME"]

    if (
        project_parameters
        and template
        and template not in project_parameters["templates"]
    ):
        project_parameters["templates"].append(template)
    elif template and "templates" not in project_parameters:
        project_parameters["templates"] = [template]

    # we iterate the rest of the parameters, and augument the projectParameters
    for i in range(len(parameters)):
        m = PARAM_RE.match(parameters[i])
        param_name = m.group(1)
        param_value = m.group(3) if m.group(3) else True

        project_parameters[param_name] = param_value
        project_parameters[f"arg{i}"] = parameters[i]

    for project_name in project_parameters["templates"]:
        project_definition: ProjectDefinition = read_project_definition(
            ARS_PROJECTS_FOLDER, project_name
        )

        # Generate the actual project.
        print(
            cyan("Generating"),
            cyan(project_name, bold=True),
            cyan("with"),
            cyan(str(project_parameters), bold=True),
        )

        if project_definition.generate_ars and ars:
            with open(".ars", "w", encoding="utf8") as json_file:
                yaml.safe_dump(project_parameters, json_file)

        process_folder(
            ".",
            project_definition.file_resolver(),
            project_parameters,
            auto_resolve_conflicts=auto,
            keep_current_files_on_conflict=keep,
        )

        for command in project_definition.shell_commands:
            print(cyan("Running"), cyan(command, bold=True))
            template = pybars.Compiler().compile(command)
            rendered_command = template(project_parameters)
            os.system(rendered_command)


def process_folder(
    current_path: str,
    file_resolver: FileResolver,
    project_parameters: Dict[str, Union[str, List[str]]],
    auto_resolve_conflicts: bool,
    keep_current_files_on_conflict: bool,
) -> None:
    """
    Recursively process the handlebars templates for the given project.
    """
    for file_entry in file_resolver.listdir():
        file: ParsedFile = parse_file_name(file_entry.name, project_parameters)

        full_local_path = os.path.join(current_path, file.name)
        full_file_path = file_entry.absolute_path

        if file_entry.name == "HELP.md" or file_entry.name == ".ars":
            print(cyan("Ignoring file        :"), cyan(file_entry.name, bold=True))
            continue

        if file_entry.is_dir:
            if os.path.isdir(full_local_path):
                print(cyan("Already exists folder:"), cyan(full_local_path, bold=True))
            else:
                print(
                    yellow("Creating folder      :"), yellow(full_local_path, bold=True)
                )
                os.makedirs(full_local_path)

            process_folder(
                full_local_path,
                file_resolver.subentry(file_entry),
                project_parameters,
                auto_resolve_conflicts,
                keep_current_files_on_conflict,
            )
            continue

        if file.keep_existing and os.path.isfile(full_local_path):
            print(cyan("Keeping regular file :"), cyan(full_local_path, bold=True))
            continue

        if not file.hbs_template:
            if not os.path.isfile(full_local_path):
                if os.path.islink(full_file_path):
                    print(
                        yellow("Linking regular file :"),
                        yellow(full_local_path, bold=True),
                    )
                else:
                    print(
                        yellow("Copying regular file :"),
                        yellow(full_local_path, bold=True),
                    )

                copy_or_link(full_file_path, full_local_path)
                continue

            if filecmp.cmp(full_file_path, full_local_path):
                print(cyan("No update needed     :"), cyan(full_local_path, bold=True))
                continue

            if is_first_file_newer(full_local_path, full_file_path):
                print(
                    cyan("No update needed ") + cyan("date", bold=True) + cyan(":"),
                    cyan(full_local_path, bold=True),
                )
                continue

            # we  have  a conflict.
            if auto_resolve_conflicts:
                print(
                    red("Conflict"),
                    red("auto", bold=True),
                    red("       :"),
                    red(full_local_path, bold=True),
                )

                copy_or_link(full_file_path, full_local_path)

                continue

            if keep_current_files_on_conflict:
                print(
                    red("Conflict"),
                    red("keep", bold=True),
                    red("       :"),
                    red(full_local_path, bold=True),
                )

                os.utime(full_local_path, (now(), now()))

                continue

            full_local_path_orig = full_local_path + ".orig"
            shutil.copy(full_local_path, full_local_path_orig, follow_symlinks=True)
            copy_or_link(full_file_path, full_local_path)

            # if 'linux' in sys.platform:
            execute_diff(full_local_path, full_local_path_orig)

            print(red("Conflict resolved    :"), red(full_local_path, bold=True))
            continue

        if os.path.islink(full_file_path):
            print(red("FATAL ERROR", bold=True))
            print(red("Template link found  :"), red(full_file_path, bold=True))
            sys.exit(1)

        with open(full_file_path, "r", encoding="utf8") as template_file:
            template_content = template_file.read()

        template = pybars.Compiler().compile(template_content)
        content = template(project_parameters)

        if not os.path.isfile(full_local_path):
            print(yellow("Parsing HBS template :"), yellow(full_local_path, bold=True))

            with open(full_local_path, "w", encoding="utf8") as content_file:
                content_file.write(content)

            shutil.copystat(full_file_path, full_local_path)

            continue

        if content == open(full_local_path, "r", encoding="utf8").read():
            print(cyan("No update needed     :"), cyan(full_local_path, bold=True))
            continue

        if is_first_file_newer(full_local_path, full_file_path):
            print(
                cyan("No update needed ") + cyan("date", bold=True) + cyan(":"),
                cyan(full_local_path, bold=True),
            )
            continue

        # we  have  a conflict.
        if auto_resolve_conflicts:
            print(
                red("Conflict"),
                red("auto", bold=True),
                red("HBS    :"),
                red(full_local_path, bold=True),
            )

            with open(full_local_path, "w", encoding="utf8") as content_file:
                content_file.write(content)

            continue

        if keep_current_files_on_conflict:
            print(
                red("Conflict"),
                red("auto", bold=True),
                red("HBS    :"),
                red(full_local_path, bold=True),
            )

            os.utime(full_local_path, (now(), now()))

            continue

        # we have a conflict
        full_local_path_orig = full_local_path + ".orig"
        shutil.copy(full_local_path, full_local_path_orig, follow_symlinks=True)
        with open(full_local_path, "w", encoding="utf8") as content_file:
            content_file.write(content)

        # if 'linux' in sys.platform:
        execute_diff(full_local_path, full_local_path_orig)

        print(red("Conflict resolved HBS:"), red(full_local_path, bold=True))


def copy_or_link(source: str, target: str) -> None:
    if os.path.islink(source):
        # if the source is a link, we need to create a link pointing
        # to a relative path that matches.
        relative_link = os.readlink(source)

        if os.path.isabs(relative_link):
            relative_link = os.path.relpath(relative_link, source)

        os.symlink(relative_link, target)
        return

    shutil.copy(source, target)


if __name__ == "__main__":
    main()
