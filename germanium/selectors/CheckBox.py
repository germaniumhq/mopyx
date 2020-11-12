
from .AbstractSelector import AbstractSelector


class CheckBox(AbstractSelector):
    """
    Just a selector that finds a checkbox input by its name.
    """
    def __init__(self, name=None):
        super(CheckBox, self).__init__()
        self._input_name = name

    def get_selectors(self):
        # CSS selector.
        xpath_selector = "xpath:.//input[@type='checkbox']"

        if self._input_name:
            xpath_selector += "[@name='%s']" % self._input_name

        return [xpath_selector]
