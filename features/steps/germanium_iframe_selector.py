from behave import *

from germanium.static import *
from germanium import iframe_selector

from features.steps.asserts import *


use_step_matcher("re")


@step("I search in the default iframe for the 'Just a message in the top frame' text")
@iframe()
def step_impl(context):
    context.found_element = Text('Just a message in the top frame').element()


@step("I search for the element '(.*?)' in the @iframe named '(.*?)'")
def step_impl(context, selector, iframe_name):
    @iframe(iframe_name)
    def find_element():
        context.found_element = S(selector).element()

    find_element()


@step("I switch the iframe selector to a custom one that handles 'custom-iframe'")
def step_impl(context):
    context.current_iframe_selector = get_germanium().iframe_selector

    def custom_iframe_selector(germanium, target):
        germanium.switch_to_default_content()
        if target == "custom-iframe":
            germanium.switch_to_frame(Element("iframe").element())

    get_germanium().iframe_selector = custom_iframe_selector


@step("I switch the iframe selector to the germanium bundled default selector")
def step_impl(context):
    context.current_iframe_selector = get_germanium().iframe_selector
    get_germanium().iframe_selector = iframe_selector.DefaultIFrameSelector()
    assert get_germanium().iframe_selector != context.current_iframe_selector


@step("when I switch the iframe selector back to the tests one")
def step_impl(context):
    get_germanium().iframe_selector = context.current_iframe_selector
    assert get_germanium().iframe_selector == context.current_iframe_selector


@step("I find in iframe '(.*?)' the element with id: '(.*?)'")
def step_impl(context, iframe_name, expected_id):
    @iframe(iframe_name)
    def check_element():
        assert_true(context.found_element, "No element was found.")
        assert_equals(expected_id, context.found_element.get_attribute('id'))

    check_element()
