from .AbstractSelector import AbstractSelector


class Css(AbstractSelector):
    """
    Just a selector that finds some CSS.
    """
    def __init__(self, selector=None):
        super(Css, self).__init__()

        self._selector = selector

    def get_selectors(self):
        """ Return the CSS selector itself """
        return ["css:" + self._selector]

