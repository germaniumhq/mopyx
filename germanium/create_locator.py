import collections
import re

from selenium.webdriver.remote.webelement import WebElement

from germanium.locators import \
    XPathLocator, \
    CssLocator, \
    CompositeLocator, \
    DeferredLocator, \
    StaticElementLocator, \
    PositionalFilterLocator, \
    InsideFilterLocator, \
    AlertLocator, \
    TextLocator, \
    WindowLocator
from germanium.selectors import \
    AbstractSelector, \
    StaticElement, \
    AnyOfSelector, \
    InsideFilterSelector, \
    PositionalFilterSelector, \
    Alert, \
    Text, \
    Window

LOCATOR_SPECIFIER = re.compile(r'((\w[\w\d]*?):)(.*)', re.MULTILINE | re.DOTALL)


def _raise_bad_selector_type(selector):
    raise Exception('Unable to build locator from the selector. '
                    'The selector: %s, that is of type: %s is '
                    'not a string selector, does not inherit from '
                    'AbstractSelector, is not an Alert, nor even a '
                    'selenium WebElement or WebElement list.' % (selector, type(selector)))


def create_locator(germanium, selector, strategy='detect'):
    if selector is None:
        raise Exception("A `None` selector was passed to Germanium to create a "
                        "locator out of it. Maybe an invalid function return "
                        "is being used?")

    if strategy != 'detect':
        locator_constructor = germanium.locator_map[strategy]

        if not locator_constructor:
            raise Exception('Unable to find strategy %s. Available strategies: detect, %s' % (strategy, ', '.join(germanium.locator_map.keys())))

        return locator_constructor(germanium, selector)

    if isinstance(selector, DeferredLocator):
        if strategy is not 'detect':
            raise Exception('The locator is already constructed, but a strategy is also defined: "%s"' %
                            strategy)

        return selector

    if isinstance(selector, PositionalFilterSelector):
        left_of_filters = map(lambda x: create_locator(germanium, x),
                              selector.left_of_filters)

        right_of_filters = map(lambda x: create_locator(germanium, x),
                               selector.right_of_filters)

        above_filters = map(lambda x: create_locator(germanium, x),
                            selector.above_filters)

        below_filters = map(lambda x: create_locator(germanium, x),
                            selector.below_filters)

        return PositionalFilterLocator(
            germanium=germanium,
            locator=create_locator(germanium, selector.selector),
            left_of_filters=left_of_filters,
            right_of_filters=right_of_filters,
            above_filters=above_filters,
            below_filters=below_filters
        )

    if isinstance(selector, InsideFilterSelector):
        inside_filters = map(lambda x: create_locator(germanium, x),
                             selector.inside_filters)
        outside_filters = map(lambda x: create_locator(germanium, x),
                              selector.outside_filters)

        containing_filters = map(lambda x: create_locator(germanium, x),
                                 selector.containing_filters)

        containing_all_filters = map(lambda x: create_locator(germanium, x),
                                     selector.containing_all_filters)

        return InsideFilterLocator(
            germanium=germanium,
            locator=create_locator(germanium, selector.selector),
            inside_filters=inside_filters,
            outside_filters=outside_filters,
            containing_filters=containing_filters,
            containing_all_filters=containing_all_filters,
            without_children=selector.without_children_elements
        )

    if isinstance(selector, Text):
        return TextLocator(germanium=germanium,
                           text=selector.searched_text,
                           exact=selector.exact_match,
                           trim=selector.trim_text)

    # AnyOfSelector can contain a list of selectors, including
    # selectors that contain filtering.
    if isinstance(selector, AnyOfSelector):
        return create_composite_locator(germanium,
                                        selector,
                                        selector.selectors)

    if isinstance(selector, StaticElement):
        return StaticElementLocator(germanium, selector.static_element)

    if isinstance(selector, AbstractSelector):
        selectors = selector.get_selectors()

        # if there is only one locator, don't apply the composite.
        if len(selectors) == 1:
            return create_locator(germanium, selectors[0])

    # Any custom user selector, that inherits from the AbstractSelector
    if isinstance(selector, AbstractSelector):
        return create_composite_locator(germanium,
                                        selector,
                                        selector.get_selectors())

    if isinstance(selector, WebElement):
        return StaticElementLocator(germanium, selector)

    if isinstance(selector, Alert):
        return AlertLocator(germanium)

    if isinstance(selector, Window):
        return WindowLocator(germanium, selector)

    if hasattr(selector, '__call__'):
        return create_locator(germanium, selector())

    if isinstance(selector, collections.Iterable) and not isinstance(selector, str):
        for item in selector:
            if not isinstance(item, WebElement):
                _raise_bad_selector_type(selector)

        return StaticElementLocator(germanium, selector)

    if not isinstance(selector, str):
        _raise_bad_selector_type(selector)

    if selector == "alert":
        return AlertLocator(germanium, selector)

    # if it starts with // it's probably an XPath locator.
    if selector[0:2] == "//":
        return XPathLocator(germanium, selector)

    m = LOCATOR_SPECIFIER.match(selector)
    if m:
        locator_constructor = germanium.locator_map[m.group(2)]
        if locator_constructor:
            return locator_constructor(germanium, m.group(3))

    return CssLocator(germanium, selector)


def create_composite_locator(germanium, selector, selectors):
    # if there is only one locator, don't apply the composite.
    if len(selectors) == 1:
        return create_locator(germanium, selectors[0])

    # if we have multiple locators, apply the composite locator.
    locator_list = []
    for child_selector in selectors:
        locator_list.append(create_locator(germanium, child_selector))

    return CompositeLocator(locator_list)
