from .AbstractSelector import AbstractSelector


class XPath(AbstractSelector):
    """
    Just a selector that finds some XPath.
    """
    def __init__(self, selector=None):
        super(XPath, self).__init__()

        if not selector.startswith('//'):
            selector = "xpath:" + selector

        self._selector = selector

    def get_selectors(self):
        """ Return the XPath selector itself """
        return [self._selector]
