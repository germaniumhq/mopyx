import collections
from germanium.impl._load_script import load_script

from .DeferredLocator import DeferredLocator


class StaticElementLocator(DeferredLocator):
    def __init__(self, germanium, element):
        """ Just holds a static reference to the elements. """
        super(StaticElementLocator, self).__init__(germanium)

        if not isinstance(element, collections.Iterable):
            self._element = [element]
        else:
            self._element = element

    def _find_element(self):
        """ Returns the locally stored element. """
        element_list = self._find_element_list()

        if not element_list:
            return None

        return element_list[0]

    def _find_element_list(self):
        if not self._root_element:
            return self._element

        js_arguments = []

        code = load_script(__name__, 'inside-filter.min.js')

        js_arguments.append(code)
        js_arguments.append(0)  # ignore without_children
        js_arguments.append(1)
        js_arguments.append(self._root_element)
        js_arguments.append(0)  # no containing_elements
        js_arguments.append(0)  # no outside_elements
        js_arguments.append(0)  # no containing_all selectors
        js_arguments.append(0)  # no containing_all element/groupIds pairs

        js_arguments.append(len(self._element))
        for element in self._element:
            js_arguments.append(element)

        result_elements = self._germanium.js(*js_arguments)

        return result_elements
