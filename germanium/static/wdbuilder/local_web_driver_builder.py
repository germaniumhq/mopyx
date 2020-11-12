import germaniumdrivers
from selenium import webdriver

from germanium.impl._workaround import workaround
from germanium.wa.firefox_open_browser_with_marionette import \
    _is_use_marionette_evironment_var_set, \
    _open_local_firefox_with_marionette


@workaround(_is_use_marionette_evironment_var_set,
            _open_local_firefox_with_marionette)
def _open_local_firefox(timeout):
    firefox_capabilities = dict(webdriver.DesiredCapabilities.FIREFOX)
    firefox_capabilities['marionette'] = False
    firefox_capabilities["unexpectedAlertBehaviour"] = "ignore"

    return webdriver.Firefox(capabilities=firefox_capabilities,
                             timeout=timeout)


def _open_local_chrome(timeout):
    germaniumdrivers.ensure_driver("chrome")
    return webdriver.Chrome()


def _open_local_ie(timeout):
    germaniumdrivers.ensure_driver("ie")
    capabilities = {"requireWindowFocus": True}
    return webdriver.Ie(timeout=timeout,
                        capabilities=capabilities)


def _open_local_edge(timeout):
    germaniumdrivers.ensure_driver("edge")
    return webdriver.Edge()


def create_local_driver(browser, timeout):
    if browser.lower() == "firefox" or browser.lower() == "ff":
        web_driver = _open_local_firefox(timeout)
    elif browser.lower() == "chrome":
        web_driver = _open_local_chrome(timeout)
    elif browser.lower() == "ie":
        web_driver = _open_local_ie(timeout)
    elif browser.lower() == "edge":
        web_driver = _open_local_edge(timeout)
    else:
        raise Exception("Unknown browser: %s, only firefox, "
                        "chrome and ie are supported." % browser)

    return web_driver
