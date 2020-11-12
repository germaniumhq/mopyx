from behave import *

from germanium.static import *


use_step_matcher("re")


@step("I click on waited '(.*?)'")
def i_click_on_waited(context, selector):
    click(waited(S(selector)))
