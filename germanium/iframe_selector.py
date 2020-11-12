
class DefaultIFrameSelector(object):
    """
    An implementation of the IFrameSelector strategy that does nothing.
    """
    def select_iframe(self, germanium, iframe_name):
        if iframe_name != "default":
            raise Exception("Unknown iframe name: '%s'. Make sure you create an IFrame Selector "
                            "that you will pass when creating the GermaniumDriver, e.g.:\n"
                            "GermaniumDriver(wd, iframe_selector=MyIFrameSelector())" % iframe_name)

        germanium.switch_to_default_content()
        return iframe_name


class CallableIFrameSelector(object):
    """
    An implementation of the IFrameSelector strategy that uses the
    given callback and wraps it.
    """
    def __init__(self, callable):
        self._callable = callable

    def select_iframe(self, germanium, iframe_name):
        return self._callable(germanium, iframe_name)
