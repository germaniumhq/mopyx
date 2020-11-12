from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I look for the following css selector: (.*)')
def step_impl(context, expected_text):
    element = S(Css(expected_text)).element()

    context.found_element = element

