from germanium.util import get_attributes_g as get_attributes_impl

from .global_germanium_instance import get_instance


def get_attributes(selector, only_visible=True):
    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_attributes_impl(get_instance(),
                               selector,
                               only_visible=only_visible)
