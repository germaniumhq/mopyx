from .global_germanium_instance import *


def close_browser():
    """
    Close the currently running browser.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    get_instance().quit()
    set_instance(None)
