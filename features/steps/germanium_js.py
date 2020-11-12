
from behave import *
from selenium.webdriver.remote.webelement import WebElement

from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u'I execute js with one parameter \'(.*?)\'')
def step_impl(context, js_parameter):
    js(context.text, js_parameter)


@step(u"I execute js without any parameters")
def step_impl(context):
    context.js_evaluation_result = js(context.text)


@step(u"I got two elements, one with id textInput, and the other with id anotherTextInput.")
def step_impl(context):
    assert_true(context.js_evaluation_result)
    assert_equals(2, len(context.js_evaluation_result))
    assert_true(isinstance(context.js_evaluation_result[0], WebElement))
    assert_true(isinstance(context.js_evaluation_result[1], WebElement))
    assert_equals("textInput", context.js_evaluation_result[0].get_attribute("id"))
    assert_equals("anotherTextInput", context.js_evaluation_result[1].get_attribute("id"))

