import os
from typing import Optional

from termcolor_util import cyan, red

from project_archer.environment.read_shell_parameters import (
    project_folder,
    current_zone,
)
from project_archer.storage.project_data import read_project_yml


def list_projects(args, env, *, custom_zone: Optional[str] = None):
    folder = project_folder(args, custom_zone=custom_zone)
    zone = current_zone(args.internalRunMode) if custom_zone is None else custom_zone

    if zone:
        env.log(red("= " + zone, bold=True))

    items = list(sorted(os.listdir(folder)))

    available_zones = []
    for filename in items:
        if os.path.isdir(os.path.join(folder, filename)) and filename != "layouts":
            available_zones.append(filename)

    if available_zones:
        env.log("Available zones:")
        for available_zone in available_zones:
            env.log("- " + red(available_zone))

    env.log("Available projects:")
    for filename in items:
        if not os.path.isfile(os.path.join(folder, filename)):
            continue

        file_data = open(os.path.join(folder, filename))
        project_data = read_project_yml(file_data)
        env.log(
            "- "
            + cyan(os.path.splitext(filename)[0], bold=True)
            + ": "
            + project_data["name"]
        )
