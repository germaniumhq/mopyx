from .AbstractSelector import AbstractSelector


class JsSelector(AbstractSelector):
    """
    Just a selector that finds some elements using some
    Js code. The code must return a list of WebDriver elements.
    """
    def __init__(self, code=None):
        super(JsSelector, self).__init__()

        self._selector = "js:" + code

    def get_selectors(self):
        """ Return the JavaScript selector itself """
        return [self._selector]
