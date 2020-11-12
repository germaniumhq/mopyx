from behave import *

from features.steps.asserts import *
from germanium.static import *

use_step_matcher("re")


@step(u'I type into the following text: (.*)')
def step_impl(context, text):
    type_keys(text)


@step(u'I type into iframe in (.*) the following text: (.*)')
@iframe('iframe')
def type_text_into_iframe_name(context, locator, text):
    type_keys(text, locator)


@step(u"I try to access the iframe named '(.*?)' that is not by default defined")
def access_wrong_iframe_name(context, name):
    @iframe(name)
    def switch_iframe():
        pass

    try:
        switch_iframe()
    except Exception as e:
        context.exception_message = str(e)
        return

    assert_false('The switch_iframe should have thrown an exception since the '
                 'iframe should not be defined.')


@step("the exception message contains the text '(.*?)'")
def check_exception_message_text(context, expected_text):
    assert_true(expected_text in context.exception_message,
                'The exception text - %s, did not contained %s.' %
                (context.exception_message, expected_text))


@step(u"in the iframe the value for the (.*?) is '(.*)'")
@iframe('iframe')
def check_value(context, locator, value):
    element = S(locator).element()

    assert_true(element)
    assert_equals(value, element.get_attribute("value"))
