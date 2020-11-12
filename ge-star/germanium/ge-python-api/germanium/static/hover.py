from germanium.util import hover_g as hover_impl
from .global_germanium_instance import *


def hover(selector):
    """
    Hover the element with the given selector.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    hover_impl(get_instance(), selector)
