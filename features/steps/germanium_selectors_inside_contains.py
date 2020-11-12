from behave import *
from steps.asserts import assert_equals, assert_false

from germanium.static import *

use_step_matcher("re")


@step(u'I search for an InputText inside the div with id inputTextContainer')
def step_impl(context):
    selector = InputText().inside(Element("div", id="inputTextContainer"))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for a span outside a div')
def step_impl(context):
    selector = Element("span").outside("div")
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for an InputText inside the div element with id inputTextContainer')
def step_impl(context):
    container_div_element = Element("div", id="inputTextContainer").element()
    selector = InputText().inside(container_div_element)
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for a div containing an InputText')
def step_impl(context):
    selector = Element("div").containing(InputText("inputTextPlaceholder"))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search using CSS for an input inside the div#inputTextContainer')
def step_impl(context):
    selector = Css("input").inside("div#inputTextContainer")
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search using CSS for a div containing an InputText')
def step_impl(context):
    selector = Css("div").containing("#inputText")
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'I search for a div inside a JS selector')
def step_impl(context):
    context.found_element = Element("div").inside("js:return [document.body];").element()


@step(u'I search for a div containing a JS selector')
def step_impl(context):
    selector = Element("div").containing("js:return [document.getElementById('inputText')];")
    context.found_element = selector.element()


@step(u'I search for all the (.*?)s without children')
def step_impl(context, tag_name):
    selector = Element(tag_name).without_children()

    context.found_element_list = selector.element_list(only_visible=False)


@step(u'I search for the first input in the second div')
def step_impl(context):
    selector = Element("input", index="1").\
        inside(Element("div", index=2))

    element = selector.element()

    assert element

    context.found_element = element


@step(u'I search for a div that contains both an input and a span')
def search_for_a_div_that_contains_both_an_input_and_a_span(context):
    selector = Element("div").containing_all(
        Input, Text("only with content")
    )

    element = selector.element()

    assert element

    context.found_element = element


@step(u"I search for a div that contains a span, that contains a text '(.*?)'")
def search_for_a_text_deep_inside_a_div_and_span(context, text):
    selector = Element("div").containing(
        Css("span").containing(
            Text(text)
        )
    )

    context.found_element = selector.element()
    context.found_element_list = selector.element_list()


@step(u'I search for a div that contains a br')
def search_for_a_div_that_contains_a_br(context):
    selector = Element("div").containing("br")
    context.found_element = selector.element()


@step(u'I only get the div with id #decoyDiv')
def step_impl(context):
    assert_equals(1, len(context.found_element_list))
    assert_equals(S('#decoyDiv').element(only_visible=False),
                  context.found_element_list[0],
                  "The element found is not the same element")


@step(u'I get no elements returned')
def step_impl(context):
    assert_false(context.found_element_list)
