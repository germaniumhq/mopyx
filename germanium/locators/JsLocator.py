from selenium.webdriver.remote.webelement import WebElement

from .DeferredLocator import DeferredLocator


class JsLocator(DeferredLocator):
    """
    A JS Deferred locator. This locator will execute some JavaScript
    code in order to find the elements.
    """
    def __init__(self, germanium, code, root_element=None):
        super(JsLocator, self).__init__(germanium, root_element)

        self._code = code

    def _find_element(self):
        """
        Finds a single element using the provided JS Code.
        """
        elements = self._find_element_list()

        return elements[0]

    def _find_element_list(self):
        """
        Finds a single element using the given code.
        """
        elements = self._germanium.js(self._code, self._root_element)

        if not elements:
            return []

        if not isinstance(elements, list):
            raise Exception("Code `%s` is not returning a list of elements." % self._code)

        return elements
