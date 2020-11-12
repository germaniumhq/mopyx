from .DeferredLocator import DeferredLocator


class CompositeLocator(DeferredLocator):
    """
    A locator that will search using the locators it contains.
    """
    def __init__(self, locators, root_element=None):
        super(CompositeLocator, self).__init__(locators[0]._germanium,
                                               root_element=root_element)

        self._locators = locators

    def set_root_element(self, root_element):
        for locator in self._locators:
            locator.set_root_element(root_element)

    def _find_element(self):
        for locator in self._locators:
            element = locator.element()
            if element:
                return element
        return None

    def _find_element_list(self):
        result = []

        for locator in self._locators:
            result.extend(locator.element_list())

        return result
