from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I search for an Input left of the text "(.*?)"')
def step_impl(context, text):
    selector = Input().left_of(Text(text))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an Input left of the text element "(.*?)"')
def step_impl(context, text):
    text_element = Text(text)
    selector = Input().left_of(text_element)
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an Input right of the text "(.*?)"')
def step_impl(context, text):
    selector = Input().right_of(Text(text))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an table cell right of the text "(.*?)"')
def step_impl(context, text):
    selector = Element("td").right_of(Text(text))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for the (.*?) input text right of the text "(.*?)"')
def step_impl(context, index, text):
    indexes = {
        "first": 0,
        "second": 1,
        "third": 2,
        "fourth": 3,
        "fifth": 4,
        "sixth": 5
    }

    selector = InputText().right_of(Text(text)).element_list()[indexes[index]]
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for all the input texts above the text "(.*?)"')
def step_impl(context, text):
    context.found_elements = InputText().above(Text(text)).element_list()


@step(u'I search for all the elements left of all the elements')
def search_all_div_elements_under_table(context):
    context.found_elements = Element("*").left_of(Element("*")).element_list()


@step(u'I search for all the input texts right of the text "(.*?)"')
def step_impl(context, text):
    context.found_elements = InputText().right_of(Text(text)).element_list()


@step(u'I search for the (.*?) input text above the text "(.*?)"')
def step_impl(context, index, text):
    indexes = {
        "first": 0,
        "second": 1,
        "third": 2,
        "fourth": 3,
        "fifth": 4,
        "sixth": 5
    }

    selector = InputText().above(Text(text)).element_list()[indexes[index]]
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an InputText above the row containing text "(.*?)"')
def step_impl(context, text):
    selector = InputText().above(Element("tr", contains_text=text))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an InputText below the row containing text "(.*?)"')
def step_impl(context, text):
    selector = InputText().below(Element("tr", contains_text=text))
    element = S(selector).element()

    assert element

    context.found_element = element
