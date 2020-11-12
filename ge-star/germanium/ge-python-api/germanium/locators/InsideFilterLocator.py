from germanium.impl._load_script import load_script
from .FilterLocator import FilterLocator

from collections import OrderedDict


class InsideFilterLocator(FilterLocator):
    def __init__(self,
                 germanium,
                 locator,
                 root_element=None,
                 inside_filters=None,
                 outside_filters=None,
                 containing_filters=None,
                 containing_all_filters=None,
                 without_children=False):

        super(InsideFilterLocator, self).__init__(germanium=germanium,
                                                  root_element=root_element,
                                                  locator=locator)

        if not inside_filters:
            inside_filters = []

        if not outside_filters:
            outside_filters = []

        if not containing_filters:
            containing_filters = []

        if not containing_all_filters:
            containing_all_filters = []

        self.inside_filters = inside_filters
        self.outside_filters = outside_filters
        self.containing_filters = containing_filters
        self.containing_all_filters = list(containing_all_filters)
        self.without_children = without_children

    def _find_element(self):
        items = self._find_element_list()
        if len(items):
            return items[0]

        return None

    def _find_element_list(self):
        # Since the inside/outside/contains/without children
        # works with the DOM structure, it might be used to find
        # invisible elements. So we need to get the raw list of
        # elements.

        inside_elements = OrderedDict()
        for selector in self.inside_filters:
            element_list = selector.element_list()

            # if we have an inside element that itself can't be found,
            # don't bother to search the elements further
            if not element_list:
                return []

            for inside_element in element_list:
                inside_elements[inside_element] = 1

        # in case there are no inside_elements, we just use the regular
        # find_element_by... on the selenium instance
        if not inside_elements:
            inside_elements = OrderedDict()
            inside_elements[None] = None

        elements = OrderedDict()
        for inside_element in inside_elements:
            self._locator.set_root_element(inside_element)
            inside_found_elements = self._locator._find_element_list()

            if not inside_found_elements:
                inside_found_elements = []

            for element in inside_found_elements:
                elements[element] = 1

        elements = list(elements)

        outside_elements = OrderedDict()
        for selector in self.outside_filters:
            element_list = selector.element_list(only_visible=False)

            # if we have an outside element that itself can't be found,
            # don't bother to search the elements further
            if not element_list:
                return []

            for outside_element in element_list:
                outside_elements[outside_element] = 1

        containing_elements = OrderedDict()
        for selector in self.containing_filters:
            element_list = selector.element_list(only_visible=False)

            # if we don't have any elements that we're supposed to
            # contain, it means the selector isn't matching, so don't
            # bother, trying to find further, otherwise we will match
            # a lot of false positives.
            if not element_list:
                return []

            for containing_element in element_list:
                containing_elements[containing_element] = 1

        # `containing_all` needs to create groups for each selector
        # and then filter the resulting elements against the
        # groups.
        #
        # We will create a dictionary that holds all the elements,
        # linked with all the group indexes they belong to, as a
        # string CSV.
        #
        # The search will remove all the elements that don't contain
        # all the groups.

        group_index = -1
        containing_all_elements = OrderedDict()
        for selector in self.containing_all_filters:
            group_index += 1
            element_list = selector._find_element_list()

            # if we have things we need to contain, but the selectors
            # don't return the elements, we don't bother so we don't
            # get false positives. eg A().contains(Text("missing")) will
            # match all A elements otherwise, the contains becomes bogus.
            if not element_list:
                return []

            for containing_all_element in element_list:
                # if the same selector for a group returns the same element multiple times,
                # make sure it's in our map only once.
                if containing_all_element in containing_all_elements:
                    containing_all_elements[containing_all_element].add(str(group_index))
                    continue
                items = set()
                items.add(str(group_index))
                containing_all_elements[containing_all_element] = items

        js_arguments = []

        code = load_script(__name__, 'inside-filter.min.js')

        js_arguments.append(code)
        js_arguments.append(1 if self.without_children else 0)
        js_arguments.append(0)  # FIXME: remove
        js_arguments.append(len(containing_elements))

        for containing_element in containing_elements:
            js_arguments.append(containing_element)

        js_arguments.append(len(outside_elements))
        for outside_element in outside_elements:
            js_arguments.append(outside_element)

        js_arguments.append(len(self.containing_all_filters))  # groupCount
        js_arguments.append(len(containing_all_elements))
        for containing_all_element in containing_all_elements:
            js_arguments.append(containing_all_element)
            js_arguments.append(",".join(containing_all_elements[containing_all_element]))

        js_arguments.append(len(elements))
        for element in elements:
            js_arguments.append(element)

        result_elements = self._germanium.js(*js_arguments)

        return result_elements
