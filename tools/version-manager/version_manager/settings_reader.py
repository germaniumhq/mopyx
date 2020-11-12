from typing import Dict
import yaml
import sys
from os import path
from termcolor_util import red

from .matcher_builder import matcher_builder
from .matchers.pattern import TrackedVersionSet, TrackedVersion


def read_settings_file(
    settings_file: str, override_settings: Dict[str, str], ignore_missing_parents: bool
) -> TrackedVersionSet:
    """
    Read the configured versions from the files. If a version is defined in the
    override_settings, then that value is going to be used, instead of what's
    read from the file.

    This allows overwriting versions, regardless of where they're read from.
    """
    if not path.exists(settings_file):
        settings_file = path.join(path.dirname(settings_file), "versions.yml")

        if not path.exists(settings_file):
            report_missing_settings_file(settings_file)
            sys.exit(1)

    with open(settings_file, "r", encoding="utf-8") as stream:
        settings = list(yaml.safe_load_all(stream))[0]

    result = list()

    for name, tracked_entry in settings.items():
        try:
            tracked_version: TrackedVersion = TrackedVersion(name)
            tracked_version.version = (
                override_settings[name]
                if name in override_settings
                else parse_version(
                    tracked_entry["version"], override_settings, ignore_missing_parents
                )
            )

            tracked_files = tracked_entry["files"] if "files" in tracked_entry else {}

            for file_name in tracked_files.keys():
                tracked_file = matcher_builder(
                    tracked_version, tracked_files[file_name]
                )
                tracked_version.files[file_name] = tracked_file
        except ParentNotFound as e:
            if ignore_missing_parents:
                continue

            raise Exception("Unable to find parent", e)
        except Exception as e:
            raise Exception("Unable to read value: %s" % name, e)
        else:
            result.append(tracked_version)

    return result


def report_missing_settings_file(settings_file: str) -> None:
    print(red("%s configuration file is missing." % settings_file))


# This import is intentionally at the end, because it's a cyclic import
from .parse_version import parse_version, ParentNotFound  # NOQA
