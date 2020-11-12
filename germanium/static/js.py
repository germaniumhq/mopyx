from .global_germanium_instance import *


def js(code, *args, **kwargs):
    """
    Right click the element with the given selector.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_instance().js(code, *args, **kwargs)
