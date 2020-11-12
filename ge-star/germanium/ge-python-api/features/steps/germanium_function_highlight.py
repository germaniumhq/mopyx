from behave import *
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

from features.steps.asserts import *
from germanium.static import *

use_step_matcher("re")


@step("I highlight the element '(.*?)'")
def step_impl(context, selector):
    highlight(selector, show_seconds=3, blink_duration=1)


@step("I highlight twice the element '(.*?)'")
def step_impl(context, selector):
    highlight(selector, show_seconds=2, blink_duration=1)
    highlight(selector, show_seconds=2, blink_duration=1)
    sleep(2)


@step("I highlight also in the console the element '(.*?)'")
def step_impl(context, selector):
    js("""
    window.console = {
        log: function() {
            window._lastlog_message = arguments;
        },
        error: function() {
            window._lasterror_message = arguments;
        }
    };
    """)
    highlight(selector, console=True, show_seconds=4, blink_duration=1)


@step("the highlighted element is '(.*?)'")
def step_impl(context, selector):
    element = S(selector).element()

    def check_element():
        background_color = get_style(element, 'outlineColor')
        return Color("#00ff00") == Color(background_color)

    wait(check_element)


@step("the element highlight for the '(.*?)' is cleared correctly")
def step_impl(context, selector):
    outline_style = get_style(selector, "outlineStyle")
    assert_equals("none", outline_style)


@step("in the log the highlighted element was notified as found")
def step_impl(context):
    assert_equals(2, len(js("return window._lastlog_message")))
    assert_equals("GERMANIUM: Element with selector `#visibleDiv` was found.",
                  js("return window._lastlog_message[0];"))
    element = js("return window._lastlog_message[1]")
    assert_true(isinstance(element, WebElement))
    assert_equals("visibleDiv", get_attributes(element)['id'])


@step("in the log there is an error message notifying the element is invisible")
def step_impl(context):
    assert_equals(2, len(js("return window._lasterror_message")))
    assert_equals("GERMANIUM: Element with selector `#invisibleDiv` was found, but is not visible.",
                  js("return window._lasterror_message[0];"))
    element = js("return window._lasterror_message[1]")
    assert_true(isinstance(element, WebElement))
    assert_equals("invisibleDiv", get_attributes(element)['id'])


@step("in the log there is an error message notifying the element as non existing")
def step_impl(context):
    assert_equals(1, len(js("return window._lasterror_message")))
    assert_equals("GERMANIUM: Unable to find element with selector `#notExistingDiv`.",
                  js("return window._lasterror_message[0];"))


@step("there is an alert notifying the element as not visible")
def step_impl(context):
    wait(Alert())
    assert_equals("GERMANIUM: Element with selector `#invisibleDiv` was found, but is not visible.",
                  Alert().text())
    Alert().accept()


@step("there is no alert present")
def step_impl(context):
    assert_true(Alert().not_exists())


@step("there is an alert notifying the element as non existing")
def step_impl(context):
    wait(Alert())
    assert_equals("GERMANIUM: Unable to find element with selector `#notExistingDiv`.",
                  Alert().text())
    Alert().accept()

