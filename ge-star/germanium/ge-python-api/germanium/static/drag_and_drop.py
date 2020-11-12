from germanium.util import drag_and_drop_g

from .global_germanium_instance import get_instance


def drag_and_drop(from_selector, to_selector):
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return drag_and_drop_g(get_instance(),
                           from_selector,
                           to_selector)
