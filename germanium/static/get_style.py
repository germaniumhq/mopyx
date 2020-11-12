from germanium.util import get_style_g
from .global_germanium_instance import *


def get_style(selector, name):
    """
    Returns the resolved CSS style for the given property name.
    :param selector:
    :param name:
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_style_g(get_instance(), selector, name)
