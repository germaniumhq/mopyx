
from behave import *
from selenium import webdriver
from germaniumdrivers import ensure_driver


use_step_matcher("re")


@step("I open Firefox")
def i_open_firefox(context):
    ensure_driver("firefox")

    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    context.browser = webdriver.Firefox(capabilities=firefox_capabilities,
                                        timeout=10)


@step("I open IE")
def i_open_firefox(context):
    ensure_driver("ie")

    context.browser = webdriver.Ie(timeout=10)


@step("I open Chrome")
def i_open_firefox(context):
    ensure_driver("chrome")

    context.browser = webdriver.Chrome()


@step("I open Edge")
def i_open_firefox(context):
    ensure_driver("edge")

    context.browser = webdriver.Edge()


@step(u'I go to google')
def i_go_to_the_google_site(context):
    context.browser.get("http://google.com")


@step(u'the title is "Google"')
def check_the_title(context):
    assert context.browser.title == "Google"