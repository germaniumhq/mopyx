class Window(object):
    """
    A pseudo selector that can match on windows opened by WebDriver.
    """
    def __init__(self, title=None, id=None):
        self.title = title
        self.id = id

    def __call__(self, *args, **kwargs):
        """
        Returns the window handle ID if it exists, or false
        otherwise.
        :param args:
        :param kwargs:
        :return:
        """
        return self.exists(*args, **kwargs)

    def element(self, *argv, germanium=None, **kw):
        """
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).element(*argv, **kw)

    def element_list(self, *argv, germanium=None, **kw):
        """
        Returns the existing alert instance as a list for the given
        germanium instance. If the alert is not present, then it will
        return None. If the germanium parameter is not set it will use
        instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).element_list(*argv, **kw)

    def exists(self, *argv, germanium=None, **kw):
        """
        Returns true if an alert is present for the given germanium instance.
        If it is not present, then it will return false. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).exists(*argv, **kw)

    def not_exists(self, *argv, germanium=None, **kw):
        """
        Returns false if an alert is present for the given germanium instance.
        If it is not present, then it will return true. If the germanium parameter
        is not set it will use instead the `germanium.static.get_germanium` instance.
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).not_exists(*argv, **kw)
