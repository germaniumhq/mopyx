from .AbstractSelector import AbstractSelector
import collections


class Element(AbstractSelector):
    def __init__(self,
                 tag_name=None,
                 *args,
                 index=None,
                 id=None,
                 exact_text=None,
                 contains_text=None,
                 css_classes=None,
                 exact_attributes=None,
                 extra_xpath=None,
                 contains_attributes=None,
                 **kw):
        """ A general element selector. """
        super(Element, self).__init__()

        if exact_text and contains_text:
            raise Exception("Having the exact text to be matched, "
                            "and a partial text to be searched is not supported.")

        self.tag_name = tag_name
        self.index = index
        self.id = id
        self.exact_text = exact_text
        self.contains_text = contains_text

        if css_classes is None:
            self.css_classes = []
        elif isinstance(css_classes, str):
            self.css_classes = css_classes.split()
        elif isinstance(css_classes, collections.Iterable):
            self.css_classes = css_classes
        else:
            raise Exception("A css_classes attribute was sent that is not an `iterable` nor "
                            "`string` object. It was a `%s` with value: `%s`" % (type(css_classes), css_classes))

        self.exact_attributes = exact_attributes
        self.extra_xpath = extra_xpath
        self.contains_attributes = contains_attributes

        self._kw = kw


    def get_selectors(self):
        if not self.contains_attributes:
            self.contains_attributes = {}

        if not self.exact_attributes:
            self.exact_attributes = {}

        if self.id:
            self.exact_attributes['id'] = self.id

        if self.exact_text and self.contains_text:
            raise Exception("Having the exact text to be matched, "
                            "and a partial text to be searched is not supported.")

        xpath_locator = './/' + self.tag_name

        if self.contains_text:
            xpath_locator += "[contains(normalize-space(string()), '%s')]" % self.contains_text

        if self.exact_text:
            xpath_locator += "[string() = '%s']" % self.exact_text

        if self.css_classes is None:
            self.css_classes = []
        elif isinstance(self.css_classes, str):
            self.css_classes = self.css_classes.split()
        elif not isinstance(self.css_classes, collections.Iterable):
            raise Exception("A css_classes attribute was sent that is not an `iterable` nor "
                            "`string` object. It was a `%s` with value: `%s`" % (type(self.css_classes), self.css_classes))

        for css_class in self.css_classes:
            xpath_locator += "[contains(concat(' ', @class, ' '), ' %s ')]" % css_class

        for k, v in self.exact_attributes.items():
            xpath_locator += "[@%s = '%s']" % (k, v)

        # all the unknown attributes can be mapped to the exact attributes.
        for k, v in self._kw:
            xpath_locator += "[@%s = '%s']" % (k, v)

        for k, v in self.contains_attributes.items():
            xpath_locator += "[contains(normalize-space(@%s), '%s')]" % (k, v)

        if self.extra_xpath:
            xpath_locator += self.extra_xpath

        if isinstance(self.index, str):
            self.index = int(self.index)

        if self.index is not None:
            if self.index > 0:
                xpath_locator = '(%s)[%d]' % (xpath_locator, self.index)
            else:
                raise Exception("The number received as an index for selectors was less "
                                "or equal to 0. These are XPath indexes, so they must "
                                "start with 1. 1st item, not 0st item.")

        xpath_locator = 'xpath:' + xpath_locator

        return [xpath_locator]
