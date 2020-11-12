from germanium.util import select_file_g
from .global_germanium_instance import *


def select_file(selector, file_path, path_check=True):
    """
    Select the given path in the file input that is matched by the selector.
    :param selector:
    :param file_path:
    :param path_check:
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    select_file_g(get_instance(), selector, file_path, path_check=path_check)
