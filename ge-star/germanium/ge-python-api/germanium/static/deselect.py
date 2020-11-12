from germanium.util import deselect_g
from .global_germanium_instance import *


def deselect(selector, text=None, *args, index=None, value=None, **kw):
    """
    Type the keys specified into the element, or the currently active element.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    deselect_g(get_instance(), selector, text=text, *args, index=index, value=value, **kw)
