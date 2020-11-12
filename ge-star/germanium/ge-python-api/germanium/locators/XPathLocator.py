import collections

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .DeferredLocator import DeferredLocator


class XPathLocator(DeferredLocator):
    """
    A XPath Deferred locator.
    """
    def __init__(self, germanium, selector, root_element=None):
        super(XPathLocator, self).__init__(germanium, root_element=root_element)
        self.selector = selector

    def _find_element(self):
        """
        Find an element using the CSS locator provided at creation.
        """
        try:
            if self._root_element:
                return self._root_element.find_element_by_xpath(self.selector)
            return self._germanium.find_element_by_xpath(self.selector)
        except NoSuchElementException:
            return None

    def _find_element_list(self):
        """
        Find an element using the CSS locator
        :return:
        """
        try:
            if self._root_element:
                result = self._root_element.find_elements_by_xpath(self.selector)
            else:
                result = self._germanium.find_elements_by_xpath(self.selector)

            if isinstance(result, collections.Iterable):
                return result

            if isinstance(result, WebElement):
                return [result]

            if result is None:
                return []

            raise Exception("Expected an iterable, but found instead %s with type %s as "
                            "a return for `web_driver.find_elements_by_xpath('%s'), on "
                            "locator %s." %
                            (result,
                             type(result),
                             self.selector,
                             self))
        except NoSuchElementException:
            return None
