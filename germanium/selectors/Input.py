
from .AbstractSelector import AbstractSelector


class Input(AbstractSelector):
    """
    Just a selector that finds an input by its name.
    """
    def __init__(self, name=None):
        super(Input, self).__init__()
        self._input_name = name

    def get_selectors(self):
        # CSS selector.
        xpath_selector = "xpath:.//input"

        if self._input_name:
            xpath_selector += "[@name='%s']" % self._input_name

        return [xpath_selector]
