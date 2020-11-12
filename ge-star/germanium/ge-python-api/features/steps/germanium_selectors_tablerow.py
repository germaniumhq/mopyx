from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I search for a TableRow with a CheckBox left of text "Surname"')
def step_impl(context):
    selector = Element("tr") \
        .containing_all(Element("td", contains_text="Surname")) \
        .containing_all(CheckBox())

    element = S(selector).element()

    assert element

    context.found_element = element


@step(u"I search for a TableRow with a Button that has label 'edit'")
def step_impl(context):
    selector = Element("tr") \
        .containing(Button('edit'))

    element = S(selector).element()

    assert element

    context.found_element = element


@step(u"I search for a TableRow with a custom XPath that is (.*)")
def step_impl(context, xpath):
    selector = Element("tr") \
        .containing(XPath(xpath))
    element = S(selector).element()

    assert element

    context.found_element = element


@step(u'it throws an exception')
def step_impl(context):
    assert context.exception
    print(context.exception)
