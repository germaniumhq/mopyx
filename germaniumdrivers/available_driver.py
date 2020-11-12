import os
import os.path

from .driver_registry import get_driver_name, AvailableDriver
from .sha_hash import sha1_file


def get_available_driver_from_path(platform, browser):
    """
    Scans the path if an available driver exists for the given
    platform and browser. If it doesn't will return None. If it
    does, it will return an available driver that points to the
    path of the driver.

    :param platform:
    :param browser:
    :return:
    """
    path_folders = get_path_folders()
    searched_name = get_driver_name(platform, browser)

    if not searched_name:
        return None

    for folder in path_folders:
        available_driver = get_available_driver_from_folder(folder, searched_name)

        if available_driver:
            return available_driver

    return None


def get_available_driver_from_folder(folder, searched_name):
    if folder_contains(folder, searched_name):
        binary_path = os.path.join(folder, searched_name)

        return AvailableDriver(
            binary_path,
            sha1_file(binary_path)
        )

    return None


def get_path_folders():
    return os.environ['PATH'].split(os.pathsep)


def folder_contains(folder_name, searched_name):
    full_path = os.path.join(folder_name, searched_name)
    return os.path.exists(full_path) and os.path.isfile(full_path)
