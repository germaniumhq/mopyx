from typing import Dict
import os
import subprocess
import re
from os import path

from version_manager.matchers.pattern import TrackedVersionSet
from version_manager.util_find import find
from version_manager.settings_reader import read_settings_file

from version_manager.command_current_version import (
    is_feature_branch,
    get_current_tag_version,
)


setting_files: Dict[str, TrackedVersionSet] = dict()

PARENT_RE = re.compile(r"^parent:(.+)@(.+?)$")
UPSTREAM_RE = re.compile(r"^upstream:(.+)$")


class ParentNotFound(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


def parse_parent_path(
    version: str,
    cwd: str,
    overriden_settings: Dict[str, str],
    ignore_missing_parents: bool,
) -> str:
    items = PARENT_RE.match(version)

    if not items:
        raise Exception(
            "The version must be in the 'parent:path@propertyname' "
            "format, got instead: '%s'." % version
        )

    parent_versions_file_path = items.group(1)
    property_name = items.group(2)

    upstream_items = UPSTREAM_RE.match(items.group(1))

    if upstream_items:
        if is_feature_branch():
            return get_current_tag_version()

        # if we didn't returned we need to romeve the upstream: part
        parent_versions_file_path = upstream_items.group(1)

    full_path = path.realpath(path.join(cwd, parent_versions_file_path))

    if not path.exists(full_path):
        raise ParentNotFound("Unable to find referenced file: %s" % full_path)

    if path.isdir(full_path):
        full_path = path.join(full_path, "versions.json")

    if full_path not in setting_files:
        setting_files[full_path] = read_settings_file(
            full_path, overriden_settings, ignore_missing_parents
        )

    property_value = find(lambda it: it.name == property_name, setting_files[full_path])

    if not property_value:
        available_properties = ", ".join(
            map(lambda it: "%s@%s" % (it.name, it.version), setting_files[full_path])
        )

        raise Exception(
            "Property '%s' is not defined in %s settings file. "
            "Available properties are: %s"
            % (property_name, full_path, available_properties)
        )

    return property_value.version


def custom_rstrip(s: str) -> str:
    """
    A custom rstrip that only strips the last Enter if it exists,
    keeping the other whitespace characters. This allows outputing
    values with whitespace formatting at the end, while handling
    the most common case of a single echo with an enter.

    """
    if s and s[-1] == "\n":
        s = s[0:-1]

    return s


def parse_version_with_path(
    version: str,
    cwd: str,
    overriden_settings: Dict[str, str],
    ignore_missing_parents: bool,
) -> str:
    old_path = os.getcwd()

    if not isinstance(version, str):
        raise Exception(
            "Got version a %s of type %s, in %s" % (version, type(version), cwd)
        )

    try:
        os.chdir(cwd)

        if version.startswith("parent:"):
            return parse_parent_path(
                version, cwd, overriden_settings, ignore_missing_parents
            )

        if "`" not in version and "$" not in version:
            return custom_rstrip(version)

        command = extract_command(version)
        result: str = subprocess.check_output(["/bin/sh", "-c", command]).decode(
            "utf-8"
        )

        return custom_rstrip(result)
    finally:
        os.chdir(old_path)


def parse_version(
    version: str, overriden_settings: Dict[str, str], ignore_missing_parents: bool
) -> str:
    return parse_version_with_path(
        version, os.getcwd(), overriden_settings, ignore_missing_parents
    )


def extract_command(version: str) -> str:
    if version.startswith("`"):
        return version[1:-1]

    if version.startswith("$"):
        return version[2:-1]

    raise Exception(f"Wrong version sent as command: {version}")
