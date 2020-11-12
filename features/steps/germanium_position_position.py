from behave import *

from features.steps.asserts import *
from germanium.static import *

use_step_matcher("re")


@step("I click on the exact element of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(selector)


@step("I click on the center of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).center())


@step("I click on the top left of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).top_left())


@step("I click on the top center of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).top_center())


@step("I click on the top right of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).top_right())


@step("I click on the middle left of '(.*?)'")
def i_click_on_the_middle_left(context, selector):
    click(Box(selector).middle_left())


@step("I click on the middle right of '(.*?)'")
def i_click_on_middle_right_corner(context, selector):
    click(Box(selector).middle_right())


@step("I click on the bottom left of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).bottom_left())


@step("I click on the bottom center of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).bottom_center())


@step("I click on the bottom right of '(.*?)'")
def i_click_on_top_left_corner(context, selector):
    click(Box(selector).bottom_right())


@step("the text of the '(.*?)' is '(.*?)'")
def verify_text(context, selector, expected_text):
    if expected_text == 'inline x: 149 y: 100' or \
                    expected_text == 'absolute x: 149 y: 100':

        expected_text_150 = expected_text.replace("149", "150")

        assert_true(expected_text == get_text(selector) or
                    expected_text_150 == get_text(selector))

        return

    assert_equals(expected_text, get_text(selector))


@when("I try to get the box positions for a selector that doesn't matches")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    try:
        Box('unknownelement').get_box()
    except Exception as e:
        context.exception_message = str(e)
        return

    assert_false(True, 'Wrong get_box did not threw exception')


@step("I get the box positions for the first two rows")
def step_impl(context):
    context.first_box = Box(Css('#row11')).get_box()
    context.second_box = Box(Css('#row21')).get_box()
    pass


@step("the positions of the 2 boxes are different")
def step_impl(context):
    assert context.first_box.top() != context.second_box.top()


@then("I get an exception spelling out that my selector didn't matched")
def step_impl(context):
    assert_contains(context.exception_message,
                    "The passed selector (unknownelement) for "
                    "finding the bounding box didn't matched")