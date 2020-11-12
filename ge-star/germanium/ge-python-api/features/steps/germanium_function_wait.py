from behave import *

from germanium.static import *


@step(u'waiting for success to happen should fail')
def step_impl(context):
    wait_threw_exception = True

    try:
        wait(S('div#successContent'),
             while_not=S('div#errorContent'))
        wait_threw_exception = False
    except Exception as e:
        pass

    if not S('div#errorContent'):
        assert False

    if not wait_threw_exception:
        assert False


@step(u'waiting for error to happen should pass')
def step_impl(context):
    wait(S('div#errorContent'))


@step(u'waiting for error or success to happen should pass with array callbacks')
def step_impl(context):
    wait([S('div#successContent'), S('div#errorContent')])


@step(u'waiting for error or success to happen should pass with multiarg callbacks')
def step_impl(context):
    wait(S('div#successContent'), S('div#errorContent'))


@step(u'I wait on a closure that returns a closure that returns False')
def wait_on_a_closure_that_returns_a_closure_that_returns_false(context):
    try:
        wait(return_return_false, timeout=0.5)
        context.wait_function_call_failed = False
    except:
        context.wait_function_call_failed = True


@step(u'I wait on a while_not that returns a closure that returns False')
def wait_on_a_while_not_that_returns_a_closure_that_returns_false(context):
    try:
        wait(return_true, while_not=return_return_false)
        context.wait_function_call_failed = False
    except:
        context.wait_function_call_failed = True


@step(u'I wait on a while_not that returns a closure that throws')
def wait_on_a_while_not_that_returns_a_closure_that_returns_false(context):
    try:
        wait(return_true, while_not=return_return_throws)
        context.wait_function_call_failed = False
    except:
        context.wait_function_call_failed = True


@step('the wait function call failed')
def wait_function_call_fails(context):
    assert context.wait_function_call_failed


@step('the wait function call passed')
def wait_function_call_fails(context):
    assert context.wait_function_call_failed == False


@step(u'I wait with a while_not that has a CSS locator built with S should pass')
def step_impl(context):
    wait(True, while_not=S('#notExistingDiv'))


# Utility test functions
def return_false():
    return False


def return_return_false():
    return return_false


def return_true():
    return True


def return_return_throws():
    return return_throws


def return_throws():
    raise Exception("throw that was returned")

