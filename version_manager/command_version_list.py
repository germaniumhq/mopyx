from termcolor_util import cyan, red, eprint
import sys

from version_manager.util_find import find
from version_manager.matchers.pattern import TrackedVersionSet


def print_single_tracked_version(
    version_name: str, versions_to_process: TrackedVersionSet
) -> None:
    tracked_version = find(lambda it: it.name == version_name, versions_to_process)

    if not tracked_version:
        eprint(
            red(
                "Tracked version '%s' does not exist. Available are: "
                "%s."
                % (
                    version_name,
                    ", ".join(map(lambda it: it.name, versions_to_process)),
                )
            )
        )
        sys.exit(1)

    print(tracked_version.version)


def print_all_tracked_versions(versions_to_process: TrackedVersionSet) -> None:
    for it in versions_to_process:
        print(cyan(it.name, bold=True), "=>", cyan(it.version))
