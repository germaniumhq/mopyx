from os import path
import sys
import os
import argparse
import glob
import colorama

from version_manager.settings_reader import read_settings_file
from version_manager.options_set import get_parameter_values, get_parameters_from_file
from version_manager.matchers.pattern import Pattern
from termcolor_util import red, green, yellow, cyan, eprint

from version_manager.command_current_version import print_current_tag_version
from version_manager.command_version_list import (
    print_single_tracked_version,
    print_all_tracked_versions,
)

from typing import Dict, List, Optional, cast


class ProgramArguments(object):
    display: Optional[List[str]]
    tag_name: bool
    load: Optional[str]
    version: bool
    ignore_missing_parents: bool
    set: Optional[List[str]]
    all: bool


def main() -> None:
    colorama.init()

    parser = argparse.ArgumentParser(description="Versions processor")

    parser.add_argument(
        "--display",
        "-d",
        metavar="NAME",
        nargs=1,
        help="Display the version of a single tracked version.",
    )
    parser.add_argument(
        "--all",
        "-a",
        "--list",
        action="store_true",
        help="Display all the tracked versions and their values.",
    )
    parser.add_argument(
        "--set",
        "-s",
        nargs="+",
        metavar="NAME=VAL",
        help="Set values overriding what's in the yml files.",
    )
    parser.add_argument(
        "--load",
        "-l",
        metavar="FILE",
        help="Override versions from the given yml file.",
    )
    parser.add_argument(
        "-t",
        "--tag-name",
        "--tag",
        action="store_true",
        help="Get the current name to use in general tags. If the "
        "branch name can't be detected from the git repo, the "
        "$BRANCH_NAME environment variable will be used.",
    )
    parser.add_argument(
        "--ignore-missing-parents",
        action="store_true",
        help="Ignore missing parents, and simply don't patch the "
        "values. Upstream values are still being patched if existing.",
    )
    parser.add_argument(
        "--version", action="store_true", help="Show the program version (0.1.master)",
    )

    argv: ProgramArguments = cast(ProgramArguments, parser.parse_args(sys.argv[1:]))

    if argv.version:
        print(cyan("version-manager: 0.1.master"))
        sys.exit(0)

    if argv.tag_name:
        print_current_tag_version()
        sys.exit(0)

    default_settings_file = path.realpath(path.join(os.getcwd(), "versions.json"))
    override_parameters = get_parameters_from_file(argv.load)
    override_parameters = get_parameter_values(override_parameters, argv.set)
    versions_to_process = read_settings_file(
        default_settings_file, override_parameters, argv.ignore_missing_parents
    )

    # Display a single tracked version
    if argv.display:
        print_single_tracked_version(argv.display[0], versions_to_process)
        sys.exit(0)

    # Display all tracked versions.
    if argv.all:
        print_all_tracked_versions(versions_to_process)
        sys.exit(0)

    eprint(cyan("Running on %s" % sys.version))

    files_to_process: Dict[str, List[Pattern]] = dict()

    for tracked_version in versions_to_process:
        for file_name, version_pattern in tracked_version.files.items():
            resolved_names = glob.glob(file_name)

            if not resolved_names:
                print(red("Unable to find any files for glob %s." % file_name))
                sys.exit(2)

            for resolved_name in resolved_names:
                if resolved_name in files_to_process:
                    file_patterns = files_to_process[resolved_name]
                else:
                    file_patterns = []
                    files_to_process[resolved_name] = file_patterns

                file_patterns.append(version_pattern)

    for resolved_name, version_patterns in files_to_process.items():
        with open(resolved_name, "r", encoding="utf-8") as resolved_file:
            content = resolved_file.read()
            new_content = content

        print(cyan("Patching %s:" % resolved_name))

        for version_pattern in version_patterns:
            tracked_version = version_pattern.tracked_version
            print(green("* %s@%s" % (tracked_version.name, tracked_version.version)))

            new_content = version_pattern.apply_pattern(new_content)

            if version_pattern.match_count != version_pattern.expected_count:
                print(
                    red(
                        "Got %d matches instead of %d."
                        % (version_pattern.match_count, version_pattern.expected_count)
                    )
                )
                sys.exit(3)

        if content == new_content:
            print(
                cyan("Content for %s is not changed. Won't patch it." % resolved_name)
            )
            continue

        with open(resolved_name, "w", encoding="utf-8") as output:
            output.write(new_content)

        print(yellow("Updated %s" % resolved_name))

    colorama.deinit()
    sys.exit(0)


if __name__ == "__main__":
    main()
