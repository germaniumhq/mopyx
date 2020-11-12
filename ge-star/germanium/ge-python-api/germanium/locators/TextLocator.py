from germanium.impl._load_script import load_script

from .DeferredLocator import DeferredLocator


class TextLocator(DeferredLocator):
    """
    A Text locator. This locator will execute some JavaScript
    code in order to find the elements.
    """
    def __init__(self,
                 germanium,
                 root_element=None,
                 text=None,
                 exact=False,
                 trim=False):
        super(TextLocator, self).__init__(germanium, root_element)
        self._searched_text = text
        self._exact_match = exact
        self._trim_text = trim

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
        code = load_script(__name__, 'text.min.js')

        elements = self._germanium.js(code,
                                      self._root_element,
                                      self._searched_text,
                                      self._exact_match,
                                      self._trim_text)

        if not elements:
            return []

        if not isinstance(elements, list):
            raise Exception("Code `%s` is not returning a list of elements." % self._code)

        return elements
