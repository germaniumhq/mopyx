import collections

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from .DeferredLocator import DeferredLocator


class CssLocator(DeferredLocator):
    """
    A CSS Deferred locator.
    """
    def __init__(self, germanium, selector, root_element=None):
        super(CssLocator, self).__init__(germanium, root_element=root_element)

        self._selector = selector

    def _find_element(self):
        """
        Find an element using the CSS locator provided at creation.
        """
        try:
            if self._root_element:
                return self._root_element.find_element_by_css_selector(self._selector)
            return self._germanium.find_element_by_css_selector(self._selector)
        except WebDriverException:
            return None

    def _find_element_list(self):
        """
        Find an element using the CSS locator provided at creation.
        """
        try:
            if self._root_element:
                result = self._root_element.find_elements_by_css_selector(self._selector)
            else:
                result = self._germanium.find_elements_by_css_selector(self._selector)

            if isinstance(result, collections.Iterable):
                return result

            if isinstance(result, WebElement):
                return [result]

            if result is None:
                return []

            raise Exception("Expected an iterable, but found instead %s with type %s as "
                            "a return for `web_driver.find_elements_by_css_selector('%s'), on "
                            "locator %s." %
                            (result,
                             type(result),
                             self._selector,
                             self))
        except WebDriverException:
            return None
