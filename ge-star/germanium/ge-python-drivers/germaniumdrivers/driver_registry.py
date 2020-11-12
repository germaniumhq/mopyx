import pkg_resources

from .configurable_settings import is_germanium_use_ie_driver_for_platform
from .sha_hash import sha1_file, sha1_data


class AvailableDriver(object):
    def __init__(self, path, sha1sum):
        self.path = path
        self.sha1sum = sha1sum


def get_driver_name(platform, browser):
    if platform.operating_system == "linux":
        if browser == "chrome":
            return "chromedriver"
        elif browser == "firefox":
            return "geckodriver"
        else:
            return None
    elif platform.operating_system == "mac":
        if browser == "chrome":
            return "chromedriver"
        elif browser == "firefox":
            return "geckodriver"
        else:
            return None
    elif platform.operating_system == "win":
        if browser == "chrome":
            return "chromedriver.exe"
        elif browser == "firefox":
            return "geckodriver.exe"
        elif browser == "ie":
            return "IEDriverServer.exe"
        elif browser == "edge":
            return "MicrosoftWebDriver.exe"
        else:
            return None
    else:
        return None


def get_internal_driver_path(platform, browser):
    if browser == "chrome":
        if platform.operating_system == "linux":
            if platform.bits == "32":
                return "binary/chrome/linux/32/chromedriver"
            elif platform.bits == "64":
                return "binary/chrome/linux/64/chromedriver"
            else:
                raise unknown_browser(platform, browser)
        elif platform.operating_system == "mac":
            return "binary/chrome/mac/64/chromedriver"
        elif platform.operating_system == "win":
            return "binary/chrome/win/32/chromedriver.exe"
        else:
            raise unknown_browser(platform, browser)
    elif browser == "firefox":
        if platform.operating_system == "linux":
            return "binary/firefox/linux/64/geckodriver"
        elif platform.operating_system == "mac":
            return "binary/firefox/mac/32/geckodriver"
        elif platform.operating_system == "win":
            return "binary/firefox/win/64/geckodriver.exe"
        else:
            raise unknown_browser(platform, browser)
    elif browser == "ie":
        if platform.operating_system == "win":
            if not is_germanium_use_ie_driver_for_platform():
                return "binary/ie/win/32/IEDriverServer.exe"
            elif platform.bits == "32":
                return "binary/ie/win/32/IEDriverServer.exe"
            elif platform.bits == "64":
                return "binary/ie/win/64/IEDriverServer.exe"
    elif browser == "edge":
        return "https://download.microsoft.com/download/3/2/D/32D3E464-F2EF-490F-841B-05D53C848D15/MicrosoftWebDriver.exe"  #EDGE

    raise unknown_browser(platform, browser)


def get_internal_driver_sha1(platform, browser):
    if browser == "edge":
        return "6f9e81e5f60fa3e8dccba15a3715ba20d44d0775"

    internal_driver_path = get_internal_driver_path(platform, browser)
    return sha1_data(pkg_resources.resource_stream(__name__, internal_driver_path).read())


def is_driver_up_to_date(platform, browser, available_driver):
    if isinstance(available_driver, AvailableDriver):
        available_driver_sha1sum = available_driver.sha1sum
    else:
        available_driver_sha1sum = sha1_file(available_driver)

    internal_sha1sum = get_internal_driver_sha1(platform, browser)

    return internal_sha1sum == available_driver_sha1sum


def unknown_browser(platform, browser):
    raise Exception(
        "Unable to find driver for %s on %s bits, for browser %s." % (
            platform.operating_system,
            platform.bits,
            browser
        ))
