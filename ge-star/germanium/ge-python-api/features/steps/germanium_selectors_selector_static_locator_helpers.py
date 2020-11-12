from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I search using selectors for an InputText right of the text "(.*?)"')
def step_impl(context, text):
    element = InputText().right_of(Text(text)).element()

    assert element

    context.found_element = element


@step(u'I search using selectors for all InputText elements')
def step_impl(context):
    context.found_elements = InputText().element_list()


@step(u'I search using selectors if an InputText right of the text "Surname" exists')
def step_impl(context):
    context.does_element_exist = InputText().right_of(Text("Surname")).exists()


@step(u'I search using selectors if an Image above the text "Surname" exists')
def step_impl(context):
    context.does_element_exist = Image().above(Text("Surname")).exists()


@step(u'yes, it exists')
def step_impl(context):
    assert context.does_element_exist


@step(u"no, it doesn't exists")
def step_impl(context):
    assert not context.does_element_exist


@step(u"I search using a Css selector for the 3rd 'input'")
def step_impl(context):
    context.found_element = Css('input').element_list(3)
