from behave import *
from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u"the '(.*?)' style from element '(.*?)' is '(.*?)'")
def step_impl(context, style_name, selector, expected_value):
    assert_equals(expected_value, get_style(selector, style_name))


@step(u"the '(.*?)' style color from element '(.*?)' is '(.*?)'")
def step_impl(context, style_name, selector, expected_value):
    assert_equals(Color(expected_value), Color(get_style(selector, style_name)))
