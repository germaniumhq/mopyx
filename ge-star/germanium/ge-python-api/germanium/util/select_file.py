from os.path import exists, abspath

from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object


def select_file_g(context, selector, file_path, path_check=True):
    absolute_path = abspath(file_path)

    if path_check and not exists(absolute_path):
        raise Exception("File '%s' does not exist. You need to pass the path to the "
                        "file that you want to select in the file input." % absolute_path)

    germanium = find_germanium_object(context)
    select_element = _element(germanium, selector)

    select_element.send_keys(absolute_path if path_check else file_path)
