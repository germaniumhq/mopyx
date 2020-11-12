from .global_germanium_instance import *


def S(*argv, germanium=None, **kwargs):
    """
    Call the super selector from germanium.
    :param germanium: The germanium instance. If missing, uses the global get_instance()
    """
    if germanium:
        return germanium.S(*argv, **kwargs)

    if not get_instance():
        raise Exception("You need to start a browser first with open_browser()")

    return get_instance().S(*argv, **kwargs)
