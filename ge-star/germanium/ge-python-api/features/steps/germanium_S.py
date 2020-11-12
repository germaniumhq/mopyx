from germanium.static import *
from germanium.locators import StaticElementLocator
from behave import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u'I search using S for (?P<locator>.*)')
def step_impl(context, locator):
    print("Search for locator: %s" % locator)
    S(locator).exists()


@step(u"the selector '(.*?)' exists somewhere")
def step_impl(context, selector):
    assert S(selector).exists(only_visible=False)


@step(u"the selector '(.*?)' exists and is visible")
def step_impl(context, selector):
    assert S(selector).exists()


@step(u"the selector '(.*?)' doesn't exists at all")
def step_impl(context, selector):
    assert S(selector).not_exists(only_visible=False)


@step(u"the selector '(.*?)' doesn't exists as visible")
def step_impl(context, selector):
    assert Css(selector).not_exists()


@step(u'nothing happens')
def step_impl(context):
    pass


@step(u"I search using a nested locator for '(.*?)'")
def step_impl(context, selector):
    element = S(S(selector)).element()

    context.found_element = element


@step(u"I search using a callable that returns a CssSelector '(.*?)'")
def step_impl(context, selector):
    def fn():
        return Css(selector)

    element = S(fn).element()

    context.found_element = element


@step(u"I search for the 3rd element that is an 'input'")
def step_impl(context):
    element = S('input').element_list(2)

    context.found_element = element


@step(u"I create a StaticElementLocator with a single element: (.*?)")
def step_impl(context, selector):
    element = S(selector).element()
    context.static_element_locator = StaticElementLocator(get_germanium(), element)


@step(u"the StaticElementLocator has one element")
def step_impl(context):
    assert_true(context.static_element_locator, "The static element locator is not found. "
                                                "Call first: I create a StaticElementLocator with a single element")
    locator = context.static_element_locator
    assert_true(locator.element())


@step(u"the StaticElementLocator has no elements anymore")
def step_impl(context):
    assert_true(context.static_element_locator, "The static element locator is not found. "
                                                "Call first: I create a StaticElementLocator with a single element")
    locator = context.static_element_locator
    assert_false(locator.element())


