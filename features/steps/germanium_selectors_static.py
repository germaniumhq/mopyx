from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u"I have a static selector for the '(.*?)'")
def static_selector_for_one_element(context, selector):
    context.static_element_selector = StaticElement(S(selector).element())


@step(u"the static element locator returns the same element as '(.*?)'")
def static_element_locator_for_same_element(context, selector):
    found_element = S(context.static_element_selector).element()
    target_element = S(selector).element()

    assert found_element
    assert found_element == target_element


@step(u"I have a static selector for all the '(.*?)' elements, including the invisible")
def static_selector_for_all_elements(context, selector):
    context.static_element_selector = StaticElement(S(selector).element_list(only_visible=False))


@step(u"search the static selector")
def search_the_static_selector(context):
    context.found_elements = context.static_element_selector.element_list()


@step(u"I search the static selector inside a table")
def search_static_selector_inside_a_table(context):
    context.found_element = None
    context.exception = None

    try:
        static_selector = context.static_element_selector
        inside_selector = static_selector.inside(Element('table'))

        context.found_element = inside_selector.element()
    except Exception as e:
        context.exception = e
