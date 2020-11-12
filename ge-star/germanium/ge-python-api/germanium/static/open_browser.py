import re

import germaniumdrivers
from selenium import webdriver

from germanium.driver import GermaniumDriver
from germanium.iframe_selector import DefaultIFrameSelector
from germanium.impl._workaround import workaround
from germanium.wa.firefox_open_browser_with_marionette import \
    _is_use_marionette_evironment_var_set, \
    _open_local_firefox_with_marionette
from .global_germanium_instance import *
from .wdbuilder.remote_web_driver_url_only_builder import create_url_remote_driver
from .wdbuilder.local_web_driver_builder import create_local_driver
from .wdbuilder.remote_web_driver_query_builder import \
    is_url_with_query_parameters, \
    create_query_parameters_remote_driver


REMOTE_ADDRESS = re.compile(r"^(\w+?):(.*?)$")


def open_browser(browser="Firefox",
                 wd=None,
                 iframe_selector=DefaultIFrameSelector(),
                 screenshot_folder="screenshots",
                 scripts=list(),
                 timeout=60):
    """
    Open the given browser.
    :param browser:
    :param wd:
    :param iframe_selector:
    :param screenshot_folder:
    :param scripts:
    """
    if get_instance():
        raise Exception("A browser already runs. Close it first with close_browser()")

    remote_match = REMOTE_ADDRESS.match(browser)

    if wd:
        web_driver = wd
    elif is_url_with_query_parameters(browser):
        web_driver = create_query_parameters_remote_driver(browser)
    elif remote_match:
        web_driver = create_url_remote_driver(remote_match)
    else:
        web_driver = create_local_driver(browser, timeout)

    set_instance(GermaniumDriver(web_driver,
                                 iframe_selector=iframe_selector,
                                 screenshot_folder=screenshot_folder,
                                 scripts=scripts))

    return get_instance()
