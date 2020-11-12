from behave import *
from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u"I get the text from element '(.*?)'")
def step_impl(context, selector):
    e = S(selector).element(only_visible=False)
    context.element_text = get_text(e)


@step(u"the text from that element is")
def step_impl(context):
    assert_equals(context.text, context.element_text)


@step(u"I get the text for a None selector")
def step_impl(context):
    test_failed = False

    try:
        get_text(None)
        test_failed = True
    except Exception as e:
        context.caught_exception = str(e)

    assert not test_failed


@step(u'I get an exception saying the selector is not defined')
def step_impl(context):
    assert_equals(context.caught_exception,
                  'The passed selector was null for the get_text() call. '
                  'If you are using it in combination with waited() (e.g. '
                  'get_text(waited(...)), it means waited could find the element.')


@step(u"I get the text for a selector that doesn't matches anything")
def step_impl(context):
    test_failed = False

    try:
        get_text(Element('not-existing'))
        test_failed = True
    except Exception as e:
        context.caught_exception = str(e)

    assert not test_failed


@step(u"I get an exception saying the selector didn't return anything")
def step_impl(context):
    assert_equals(context.caught_exception,
                  'No items, visible or invisible, matched the '
                  'selector given for the action.')
