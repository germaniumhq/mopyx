from behave import *
from time import sleep
import os
import re
import threading

from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


URL_MATCHER=re.compile(r"^(https?://)(.*?)(/.*)$")


def instantiate_germanium_webdriver():
    browser = "firefox"

    if 'TEST_BROWSER' in os.environ:
        browser = os.environ['TEST_BROWSER']

    def iframe_selector(germanium, iframe_name):
        if iframe_name == 'iframe':
            iframe = germanium.S('iframe').element()
            germanium.switch_to_frame(iframe)
        else:
            germanium.switch_to_default_content()

    open_browser(browser,
                 iframe_selector=iframe_selector)


@step("I open the browser")
def open_browser_step(context):
    """
    :param context:
    :return: void
    """
    if not get_germanium():
        instantiate_germanium_webdriver()


@step("I go to '(?P<page>.*?)'")
@step("I navigate to '(?P<page>.*?)'")
def navigate_to_page(context, page):
    """
    Navigate to the given URL.
    :param context:
    :param page:
    :return:
    """
    if 'TEST_HOST' in os.environ:
        page_matcher = URL_MATCHER.match(page)
        page = page_matcher.group(1) + \
               os.environ['TEST_HOST'] + \
               page_matcher.group(3)

    go_to(page)


@step(u'I type \'(?P<keys>.*?)\' into (?P<selector>.*)')
def type_keys_with_selector(context, keys, selector):
    type_keys(keys, selector)


@step(u'the value for the (?P<selector>.*) is \'(?P<value>.*?)\'')
def step_impl(context, selector, value):
    element = S(selector).element()

    assert_equals(value, get_value(element))


@step("the title of the page equals '(?P<what>.*?)'")
def check_title_page(context, what):
    assert_equals(what, get_germanium().title)


@step(u'I type_keys \'(?P<what>.*?)\'')
def type_keys_impl(context, what):
    type_keys(what)


@step(u"in the selector (.*?) I type_keys '(.*?)'")
def type_keys_impl(context, selector, keys):
    type_keys(keys, selector)


@step(u"in the locator (.*?) I type_keys '(.*?)'")
def type_keys_impl(context, selector, keys):
    type_keys(keys, S(selector))


@step(u"in the locator (.*?) I type_keys '(.*?)' with 200ms delay")
def type_keys_impl(context, selector, keys):
    type_keys(keys, S(selector), delay=0.2)


@step(u"I click on '(.*)'")
def step_impl(context, selector):
    click(selector)


@step(u'the text of the page is')
def step_impl(context):
    assert_equals(context.text, Element('body').element().text)


@step(u"the text of the page contains '(.*?)'")
def step_impl(context, text):
    assert_true(text in Element('body').text())


@step(u"the text of the page doesn't contain '(.*?)'")
def step_impl(context, text):
    assert_true(text not in Element('body').text())


@step(u'I wait forever')
def step_impl(context):
    sleep(10000000)


@step(u'the I can read from a different thread the title of the page as \'(.*?)\'')
def step_impl(context, title):

    def check_title():
        assert_equals(title, get_germanium().title)

    t = threading.Thread(target=check_title)
    t.start()
    t.join()
