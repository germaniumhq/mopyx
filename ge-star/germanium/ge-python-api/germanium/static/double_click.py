from germanium.util import double_click_g as double_click_impl
from .global_germanium_instance import *


def double_click(selector):
    """
    Double click the element with the given selector.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    double_click_impl(get_instance(), selector)
