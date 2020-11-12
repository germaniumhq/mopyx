from .DeferredLocator import DeferredLocator


class FilterLocator(DeferredLocator):
    def __init__(self, germanium=None, root_element=None, locator=None):
        super(FilterLocator, self).__init__(germanium=germanium,
                                            root_element=root_element)
        self._locator = locator

    def set_root_element(self, root_element):
        self._locator.set_root_element(root_element)
        return self
