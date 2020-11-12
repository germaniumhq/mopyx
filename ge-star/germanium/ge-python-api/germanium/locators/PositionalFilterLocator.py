from .FilterLocator import FilterLocator
from germanium.impl._load_script import load_script

from collections import OrderedDict


class PositionalFilterLocator(FilterLocator):
    def __init__(self,
                 germanium,
                 locator,
                 root_element=None,
                 left_of_filters=None,
                 right_of_filters=None,
                 above_filters=None,
                 below_filters=None):

        super(PositionalFilterLocator, self).__init__(germanium=germanium,
                                                      root_element=root_element,
                                                      locator=locator)

        if not left_of_filters:
            left_of_filters = []

        if not right_of_filters:
            right_of_filters = []

        if not above_filters:
            above_filters = []

        if not below_filters:
            below_filters = []

        self.locator = locator
        self.left_of_filters = left_of_filters
        self.right_of_filters = right_of_filters
        self.above_filters = above_filters
        self.below_filters = below_filters

    def _find_element(self):
        items = self._find_element_list()
        if len(items):
            return items[0]

        return None

    def _find_element_list(self):
        # Since this filter sorts elements that would appear visually right of
        # or left of things, we don't need to get the raw element list using
        # `_find_element_list` but we can work with the filtered list.
        elements = self.locator.element_list()

        left_of_elements = OrderedDict()
        for selector in self.left_of_filters:
            for left_of_element in selector.element_list():
                left_of_elements[left_of_element] = 1

        right_of_elements = OrderedDict()
        for selector in self.right_of_filters:
            for right_of_element in selector.element_list():
                right_of_elements[right_of_element] = 1

        above_elements = OrderedDict()
        for selector in self.above_filters:
            for above_element in selector.element_list():
                above_elements[above_element] = 1

        below_elements = OrderedDict()
        for selector in self.below_filters:
            for below_element in selector.element_list():
                below_elements[below_element] = 1

        js_arguments = []

        code = load_script(__name__, 'positional-filter.min.js')

        js_arguments.append(code)
        js_arguments.append(len(above_elements))
        for above_element in above_elements:
            js_arguments.append(above_element)
        js_arguments.append(len(right_of_elements))
        for right_of_element in right_of_elements:
            js_arguments.append(right_of_element)
        js_arguments.append(len(below_elements))
        for below_element in below_elements:
            js_arguments.append(below_element)
        js_arguments.append(len(left_of_elements))
        for left_of_element in left_of_elements:
            js_arguments.append(left_of_element)
        js_arguments.append(len(elements))
        for element in elements:
            js_arguments.append(element)

        result_elements = self._germanium.js(*js_arguments)

        return result_elements
