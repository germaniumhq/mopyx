import re
import urllib.parse as urlparse

from selenium import webdriver
from ._germanium_remote import \
    GermaniumRemote, \
    _create_remote_firefox_capabilities


REMOTE_QUERY_PATTERN = re.compile("^(\\w+?)\\?(.*?)$")
WD_URL = "wdurl"


class BrowserSpecification(object):
    def __init__(self):
        self.browser_name = ""
        self.url = ""
        self.desired_capabilities = {}
        self.required_capabilities = {}


def query_uri_parse(browser_string):
    m = REMOTE_QUERY_PATTERN.match(browser_string)

    if not m:
        raise Exception("UriParser called on a non URI.")

    result = BrowserSpecification()

    result.browser_name = m.group(1)
    query_params = urlparse.parse_qs(urlparse.urlsplit(browser_string).query)

    for name, values in query_params.items():
        if not values:
            result.desired_capabilities[name] = 'true'

        if name == WD_URL:
            result.url = values[0]
            continue

        result.desired_capabilities[name] = values[0]

    if not result.url:
        raise Exception(
            "Unable to create a remote browser from: `%s`. In order to create a "
            "browser, the `%s` must be specified in the query parameters."
            % (browser_string, WD_URL))

    return result


def is_url_with_query_parameters(browser):
    return REMOTE_QUERY_PATTERN.match(browser)


def create_query_parameters_remote_driver(browser_string):
    browser_specification = query_uri_parse(browser_string)

    remote_browser = browser_specification.browser_name

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
                        "chrome ie and edge are supported." % remote_browser)

    for key, value in browser_specification.desired_capabilities.items():
        remote_capabilities[key] = value

    return GermaniumRemote(command_executor=browser_specification.url,
                           desired_capabilities=remote_capabilities)
