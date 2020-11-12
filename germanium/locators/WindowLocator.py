
class WebDriverWindow(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class WindowLocator(object):
    """
    Create a deferred locator that can be used in matching
    elements in wait conditions, to wait for windows to open.
    """
    def __init__(self, germanium=None, selector=None):
        self._germanium = germanium
        self._selector = selector

    def __call__(self):
        return self.exists()

    def element(self, only_visible=True):
        """
        Return the window that matches the given selector, it it
        exists.
        :return:
        """
        result_list = self.element_list(only_visible=only_visible)
        if result_list:
            return result_list[0]

        return None

    def element_list(self, only_visible=True):
        """
        Returns all the windows that match the given selector, or an
        empty list if no window exists.
        :param only_visible: Ignored. Kept for compatibility with locators API.
        :return:
        """
        if self._selector.id:
            if not self._selector.id in self._germanium.window_handles:
                return []

            current_handle = self._germanium.current_window_handle
            self._germanium.switch_to.window(self._selector.id)

            result = WebDriverWindow(self._selector.id,
                                     self._germanium.title)

            self._germanium.switch_to.window(current_handle)

            return [result]

        result_list = []
        current_handle = self._germanium.current_window_handle

        # find all the handles
        for handle in self._germanium.window_handles:
            self._germanium.switch_to.window(handle)
            window_title = self._germanium.title

            # if the selector title is None, it means we need to find
            # all the opened windows, since the id is already checked
            # on the selector as being None.
            if self._selector.title is None:
                result_list.append(WebDriverWindow(handle, window_title))
                continue

            if window_title == self._selector.title:
                result_list.append(WebDriverWindow(handle, window_title))

        self._germanium.switch_to_window(current_handle)

        return result_list

    def exists(self):
        """
        Returns true if an alert is present.
        :return:
        """
        return bool(self.element())

    def not_exists(self):
        """
        Returns false if alert exists.
        :return:
        """
        return not self.exists()
