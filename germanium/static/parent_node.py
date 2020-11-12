from germanium.util import parent_node_g
from .global_germanium_instance import *


def parent_node(selector):
    """
    Finds the parent_node of the given selector.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return parent_node_g(get_instance(), selector)
