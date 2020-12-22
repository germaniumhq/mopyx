from typing import Dict, Union
import os

from PySide2 import QtGui

from germanium_build_monitor.resources import base_dir
from germanium_build_monitor.model.BuildStatus import BuildStatus
from germanium_build_monitor.model.JenkinsJobBranch import JenkinsJobBranch
from germanium_build_monitor.model.RootModel import RootModel


icon_cache: Dict[str, QtGui.QIcon] = dict()


def get_icon(icon_name: str) -> QtGui.QIcon:
    if icon_name in icon_cache:
        return icon_cache[icon_name]

    icon = create_icon(icon_name)

    icon_cache[icon_name] = icon

    return icon


def build_status_icon(status: BuildStatus) -> QtGui.QIcon:
    if status == BuildStatus.SUCCESS:
        return get_icon("build_succeded.png")
    elif status == BuildStatus.FAILURE:
        return get_icon("build_failed.png")
    elif status == BuildStatus.RUNNING:
        return get_icon("unknown_builds_in_progress.png")
    elif status == BuildStatus.NEVER:
        return get_icon("build_ignored.png")
    elif status == BuildStatus.IGNORED:
        return get_icon("build_ignored.png")
    else:
        raise Exception(f"Unsupported value {status}")


def aggregate_status_icon(branch: Union[JenkinsJobBranch, RootModel]) -> QtGui.QIcon:
    if branch.status != BuildStatus.RUNNING:
        return build_status_icon(branch.status)

    return get_icon("unknown_builds_in_progress.png")


def systray_status_icon(status: BuildStatus) -> QtGui.QIcon:
    if status == BuildStatus.SUCCESS:
        return get_icon("builds_succeding.png")
    elif status == BuildStatus.FAILURE:
        return get_icon("builds_failing.png")
    elif status == BuildStatus.RUNNING:
        return get_icon("unknown_builds_in_progress.png")
    elif status == BuildStatus.NEVER:
        return get_icon("never128.png")
    else:
        raise Exception(f"Unsupported value {status}")


def get_icon_path(icon_name: str) -> str:
    return os.path.join(base_dir(), icon_name)


def create_icon(icon_name: str) -> QtGui.QIcon:
    icon = QtGui.QIcon()
    icon_path = os.path.join(base_dir(), icon_name)

    icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    return icon
