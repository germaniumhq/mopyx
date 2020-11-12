from selenium.webdriver.remote.webelement import WebElement

from germanium.impl import _ensure_list


class AbstractSelector(object):
    """
    Just a marker interface.
    """
    def __init__(self):
        pass

    def get_selectors(self):
        raise Exception("Abstract class, not implemented.")

    def left_of(self, *argv, **kw):
        return PositionalFilterSelector(self)\
            .left_of(*argv, **kw)

    def right_of(self, *argv, **kw):
        return PositionalFilterSelector(self) \
            .right_of(*argv, **kw)

    def above(self, *argv, **kw):
        return PositionalFilterSelector(self) \
            .above(*argv, **kw)

    def below(self, *argv, **kw):
        return PositionalFilterSelector(self) \
            .below(*argv, **kw)

    def inside(self, *argv, **kw):
        return InsideFilterSelector(self) \
            .inside(*argv, **kw)

    def outside(self, *argv, **kw):
        return InsideFilterSelector(self) \
            .outside(*argv, **kw)

    def containing(self, *argv, **kw):
        return InsideFilterSelector(self) \
            .containing(*argv, **kw)

    def containing_all(self, *argv, **kw):
        return InsideFilterSelector(self) \
            .containing_all(*argv, **kw)

    def without_children(self, *argv, **kw):
        return InsideFilterSelector(self) \
            .without_children(*argv, **kw)

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
        return self.element_list(*args, **kwargs)

    def element(self, *argv, germanium=None, **kw):
        """
        If the germanium is provided, the selector is evaluated using
        germanium.S. If the germanium attribute is not provided,
        this is equivalent to: germanium.static.S(self).element()
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).element(*argv, **kw)

    def element_list(self, index=None, *argv, germanium=None, **kw):
        """
        If the germanium is provided, the selector is evaluated using
        germanium.S. If the germanium attribute is not provided,
        this is equivalent to: germanium.static.S(self).element_list()
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).element_list(index=index, *argv, **kw)

    def exists(self, *argv, germanium=None, **kw):
        """
        If the germanium is provided, the selector is evaluated using
        germanium.S. If the germanium attribute is not provided,
        this is equivalent to: germanium.static.S(self).exists()
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).exists(*argv, **kw)

    def not_exists(self, *argv, germanium=None, **kw):
        """
        If the germanium is provided, the selector is evaluated using
        germanium.S. If the germanium attribute is not provided,
        this is equivalent to: germanium.static.S(self).not_exists()
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).not_exists(*argv, **kw)

    def text(self, *argv, germanium=None, only_visible=True, **kw):
        """
        Returns the text of the `element()` returned by this selector.
        If the germanium is provided, the selector is evaluated using
        germanium.S. If the germanium attribute is not provided,
        this is equivalent to: germanium.static.S(self).text()
        :param argv:
        :param germanium:
        :param kw:
        :return:
        """
        from germanium.static import S
        return S(self, germanium=germanium).text(*argv, **kw)


class InsideFilterSelector(AbstractSelector):
    def __init__(self, parent_selector):
        super(InsideFilterSelector, self).__init__()

        self.selector = parent_selector

        self.inside_filters = []
        self.outside_filters = []
        self.containing_filters = []
        self.containing_all_filters = []
        self.without_children_elements = False

    def inside(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.inside_filters.extend(other_selector)

        return self

    def outside(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.outside_filters.extend(other_selector)

        return self

    def containing(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.containing_filters.extend(other_selector)

        return self

    def containing_all(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.containing_all_filters.extend(other_selector)

        return self

    def without_children(self, *argv, **kw):
        self.without_children_elements = True

        return self


class PositionalFilterSelector(AbstractSelector):
    """
    Filters selectors
    """
    def __init__(self, parent_selector):
        super(AbstractSelector, self).__init__()

        self.selector = parent_selector

        self.left_of_filters = []
        self.right_of_filters = []
        self.above_filters = []
        self.below_filters = []

    def left_of(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.left_of_filters.extend(other_selector)

        return self

    def right_of(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.right_of_filters.extend(other_selector)

        return self

    def above(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.above_filters.extend(other_selector)

        return self

    def below(self, *argv, **kw):
        other_selector = _ensure_selectors(argv)
        self.below_filters.extend(other_selector)

        return self


def _ensure_selectors(items):
    items = _ensure_list(items)

    for i in range(len(items)):
        items[i] = _ensure_selector(items[i])

    return items


def _ensure_selector(item):
    from .JsSelector import JsSelector
    from .XPath import XPath
    from .Css import Css

    if isinstance(item, AbstractSelector):
        return item

    if hasattr(item, '__call__'):
        return _ensure_selector(item())

    if isinstance(item, str):
        if item.startswith("js:"):
            return JsSelector(item[3:])
        elif item.startswith("xpath:"):
            return XPath(item[6:])
        elif item.startswith("//"):
            return XPath(item)
        elif item.startswith("css:"):
            return Css(item[4:])
        else:
            return Css(item)

    if isinstance(item, WebElement):
        return item

    raise Exception("The element given as a selector %s was not a valid selector"
                    "for this context." % item)
