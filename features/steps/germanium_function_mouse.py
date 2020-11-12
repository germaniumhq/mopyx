from behave import *

from germanium.static import *

use_step_matcher("re")


@step(u'I right click on (.*)')
def step_impl(context, selector):
    right_click(selector)


@step(u'I doubleclick on (.*)')
def step_impl(context, selector):
    double_click(selector)


@step(u'I mouse over on (.*)')
def step_impl(context, selector):
    hover(selector)

