from behave import *
from germanium.static import *

use_step_matcher("re")


@step(u'I look for a link with some text: \'(.*?)\'')
def step_impl(context, text):
    element = S(Link(text)).element()

    assert element

    context.found_element = element


@step(u'I look for a link with exactly the text: \'(.*?)\'')
def step_impl(context, text):
    element = S(Link(text=text)).element()

    assert element

    context.found_element = element


@step(u'I look for a link with the href: \'(.*?)\'')
def step_impl(context, href):
    element = S(Link(href=href)).element()

    assert element

    context.found_element = element


@when(u'I look for a link with the href containing: \'(.*?)\'')
def step_impl(context, href):
    element = S(Link(search_href=href)).element()

    assert element

    context.found_element = element

