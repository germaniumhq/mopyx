from .global_germanium_instance import *


def go_to(url):
    """
    Go to the given URL, and wait for the page to load.
    """
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    get_instance().get(url)
