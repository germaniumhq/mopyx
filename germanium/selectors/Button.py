from .AbstractSelector import AbstractSelector


class Button(AbstractSelector):
    """
    Just a selector that finds a button by its label or name.
    """
    def __init__(self, search_text=None, text=None, name=None):
        super(Button, self).__init__()

        self._search_text = search_text
        self._text = text
        self._name = name

        if self._search_text and self._text:
            raise Exception("You can't have both a searched text and an exact text match")

    def get_selectors(self):
        """ Return the CSS selector to find the button. """
        button_selector = "xpath:.//button"
        input_selector = "xpath:.//input[@type='button' or @type='submit']"

        if self._name:
            button_selector += "[@name='%s']" % self._name
            input_selector += "[@name='%s']" % self._name

        if self._text:
            button_selector += "[string(.)='%s']" % self._text
            input_selector += "[@value='%s']" % self._text

        if self._search_text:
            button_selector += "[contains(normalize-space(string()), \"%s\")]" % self._search_text
            input_selector += "[contains(@value, \"%s\")]" % self._search_text

        return [input_selector, button_selector]
