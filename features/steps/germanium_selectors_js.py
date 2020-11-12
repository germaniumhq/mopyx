from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I look for the following js selector: (.*)')
def step_impl(context, code):
    try:
        element = JsSelector(code).element()

        context.exception = None
        context.found_element = element
    except Exception as e:
        context.found_element = None
        context.exception = e


@step(u'I look for the following js single element selector')
def step_impl(context):
    try:
        code = context.text
        element = JsSelector(code).element(only_visible=False)

        context.exception = None
        context.found_element = element
    except Exception as e:
        context.found_element = None
        context.exception = e

