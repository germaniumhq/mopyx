from germanium.impl import wait


class Alert(object):
    def __call__(self, *args, **kwargs):
        """
        Return the element list. If germanium is provided, the selector
        is evaluated using g.S(self).element_list(). If is not
        provided, this is equivalent to
        germanium.static.S(self).element_list()
        :param args:
        :param kwargs:
        :return:
        """
        return self.exists(*args, **kwargs)

    def element(self, *argv, **kw):
        """
        Returns the existing alert instance for the given germanium instance.
        If the alert is not present, then it will return None.
        If the germanium parameter is not set it will use instead the
        `germanium.static.get_germanium` instance.
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self).element(*argv, **kw)

    def element_list(self, *argv, **kw):
        """
        Returns the existing alert instance as a list for the given
        germanium instance. If the alert is not present, then it will
        return None. If the germanium parameter is not set it will use
        instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self).element(*argv, **kw)

    def exists(self, *argv, **kw):
        """
        Returns true if an alert is present for the given germanium instance.
        If it is not present, then it will return false. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self).exists(*argv, **kw)

    def not_exists(self, *argv, **kw):
        """
        Returns false if an alert is present for the given germanium instance.
        If it is not present, then it will return true. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self).not_exists(*argv, **kw)

    def text(self, *argv, **kw):
        """
        Returns the text of the currently visible alert. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self).text(*argv, **kw)

    def accept(self, wait_disappear=True, *argv, **kw):
        """
        Accepts the current alert from the germanium instance. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param wait_disappear: Wait for the alert to not exist anymore.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S, get_germanium
        alert = S(self).element(*argv, **kw)

        wait(lambda: alert.accept() or True, timeout=1)
        get_germanium()._last_alert = None

        if wait_disappear:
            wait(self.not_exists)

    def dismiss(self, wait_disappear=True, *argv, **kw):
        """
        Dismisses (i.e. cancels) the current alert from the germanium instance.
        If the germanium parameter is not set it will use instead the
        `germanium.static.get_germanium` instance.
        :param wait_disappear: Wait for the alert to not exist anymore.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S, get_germanium
        alert = S(self).element(*argv, **kw)

        wait(lambda: alert.dismiss() or True, timeout=1)
        get_germanium()._last_alert = None

        if wait_disappear:
            wait(self.not_exists)

    def send_keys(self, text, *argv, **kw):
        """
        Types the given keys into the alert.
        If the germanium parameter is not set it will use instead the
        `germanium.static.get_germanium` instance.
        :param text: The text to type into.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S, get_germanium
        alert = S(self).element(*argv, **kw)

        alert.send_keys(text)
        get_germanium()._last_alert = None

    def authenticate(self, username, password, wait_disappear=True, *argv, **kw):
        """
        Fills in the username and password into the alert.
        If the germanium parameter is not set it will use instead the
        `germanium.static.get_germanium` instance.
        :param wait_disappear: Wait for the alert to not exist anymore.
        :param password:
        :param username:
        :param argv:
        :param kw:
        :return:
        """
        from germanium.static import S, get_germanium
        alert = S(self).element(*argv, **kw)

        wait(lambda: alert.autenticate(username, password) or True, timeout=1)
        get_germanium()._last_alert = None

        if wait_disappear:
            wait(self.not_exists)
