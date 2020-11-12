from germanium.util import child_nodes_g
from .global_germanium_instance import *


def child_nodes(selector, only_elements=True):
    """
    Finds the child nodes of the given selector.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return child_nodes_g(get_instance(), selector, only_elements=only_elements)
