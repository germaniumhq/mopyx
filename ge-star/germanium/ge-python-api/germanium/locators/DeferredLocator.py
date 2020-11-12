from germanium.impl import _filter_not_displayed


class DeferredLocator(object):
    """
    Create a deferred locator that can be used in matching
    elements in wait conditions.
    """
    def __init__(self, germanium=None, root_element=None):
        self._germanium = germanium
        self._root_element = root_element

    def __call__(self):
        return self.element_list()

    def set_root_element(self, root_element):
        self._root_element = root_element
        return self

    def element(self, only_visible=True):
        """ Return the current matched element.
        :param only_visible: bool Find the element only
        if it's visible, so it can be interacted with.
        """
        if only_visible:
            elements = self.element_list(only_visible=only_visible)
            if not elements:
                return None

            return elements[0]

        return self._find_element()

    def element_list(self, index=None, only_visible=True):
        """
        :param index: if set, return only the element with the given index.
        :type only_visible: boolean
        """
        result = _filter_not_displayed(self._germanium,
                                       self._find_element_list(),
                                       only_visible=only_visible)

        if index is not None:
            if not result or index >= len(result):
                if not result:
                    raise Exception("Unable to return the element from the element_list with index %s. "
                                    "The search returned no results." % index)
                raise Exception("Unable to return the element from the element_list with index %d. "
                                "The search returned only %d items." % (index, len(result)))

            return result[index]

        return result

    def exists(self, only_visible=True):
        """ Return True/False if the currently matched element exists or not
        :param only_visible:
        """
        return self.element(only_visible=only_visible) is not None

    def not_exists(self, only_visible=True):
        """
        :param only_visible:
        :return: True if the element is not existing.
        """
        return self.element(only_visible=only_visible) is None

    def text(self, only_visible=True):
        """
        :param only_visible:
        :return: True the text of the found element.
        """
        return self.element(only_visible=only_visible).text

    def _find_element(self):
        """ Find the element. """
        raise Exception("not implemented")

    def _find_element_list(self):
        """
        Find all the elements that match the given locator.
        :return:
        """
        raise Exception("Not implemented")
