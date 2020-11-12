
from selenium import webdriver
from ._germanium_remote import \
    GermaniumRemote, \
    _create_remote_firefox_capabilities


def create_url_remote_driver(remote_match):
    remote_browser = remote_match.group(1)

    if remote_browser.lower() == "firefox" or remote_browser.lower() == "ff":
        remote_capabilities = _create_remote_firefox_capabilities()
    elif remote_browser.lower() == "chrome":
        remote_capabilities = webdriver.DesiredCapabilities.CHROME
    elif remote_browser.lower() == "ie":
        remote_capabilities = dict(webdriver.DesiredCapabilities.INTERNETEXPLORER)
        remote_capabilities["requireWindowFocus"] = True
    elif remote_browser.lower() == "edge":
        remote_capabilities = webdriver.DesiredCapabilities.EDGE
    else:
        raise Exception("Unknown browser: %s, only firefox, "
                        "chrome, ie and edge are supported." % remote_browser)

    return GermaniumRemote(command_executor=remote_match.group(2),
                           desired_capabilities=remote_capabilities)
