from behave import *
from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u'I look for a button with the text: \'(.*?)\'')
def step_impl(context, expected_text):
    element = S(Button(expected_text)).element()

    context.found_element = element


@step(u'I look for a button with the exact text: \'(.*?)\'')
def step_impl(context, expected_text):
    element = S(Button(text=expected_text)).element()

    context.found_element = element


@step(u'I look for a button with the name: \'(.*?)\'')
def step_impl(context, expected_name):
    element = S(Button(name=expected_name)).element()

    context.found_element = element


@step(u'I find the element with id: \'(.*?)\'')
def step_impl(context, expected_id):
    assert_true(context.found_element, "No element was found.")
    assert_equals(expected_id, context.found_element.get_attribute('id'))


@step(u'I find no element')
def step_impl(context):
    assert_false(context.found_element)
    assert_false(context.exception)


@step(u'I look for some text: \'(.*)\'')
def step_impl(context, text):
    element = S(Text(text)).element()

    context.found_element = element


@step(u"I look for some text in multiple elements: '(.*?)'")
def step_impl(context, text):
    element_list = S(Text(text)).element_list()

    context.found_elements = element_list


@step(u"I look for the exact text in multiple elements: '(.*?)'")
def step_impl(context, text):
    element_list = S(Text(text, exact=True)).element_list()

    context.found_elements = element_list


@step(u"I look for the exact trimmed text in multiple elements: '(.*?)'")
def step_impl(context, text):
    element_list = S(Text(text, exact=True, trim=True)).element_list()

    context.found_elements = element_list


@step(u'there is no element found')
def step_impl(context):
    assert not context.found_element


@step(u'there are no elements found')
def step_impl(context):
    assert not context.found_elements


@step(u'I find (\d+) elements that match')
@step(u'I find (\d+) text elements that match')
def step_impl(context, count):
    assert_true(context.found_elements)
    assert_true(isinstance(context.found_elements, list))
    assert_equals(int(count), len(context.found_elements))
