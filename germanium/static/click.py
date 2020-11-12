from germanium.util import click_g as click_impl
from .global_germanium_instance import *


def click(selector):
    """
    Click the element with the given selector.
    :param selector:
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    click_impl(get_instance(), selector)
