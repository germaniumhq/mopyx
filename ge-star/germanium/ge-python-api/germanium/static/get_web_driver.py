from .global_germanium_instance import *


def get_web_driver():
    """
    Returns the currently used web_driver object by germanium.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_instance().web_driver
