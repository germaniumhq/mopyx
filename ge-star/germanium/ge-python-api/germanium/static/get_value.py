from germanium.util import get_value_g
from .global_germanium_instance import *


def get_value(selector):
    """
    Type the keys specified into the element, or the currently active element.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_value_g(get_instance(), selector)
