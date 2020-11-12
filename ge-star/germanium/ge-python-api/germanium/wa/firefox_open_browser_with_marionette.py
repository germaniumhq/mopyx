import os
import germaniumdrivers
from selenium import webdriver


def _is_use_marionette_evironment_var_set(germanium):
    return 'GERMANIUM_FIREFOX_USE_MARIONETTE' in os.environ


def _open_local_firefox_with_marionette(germanium, original_function, *args, **kw):
    timeout = args[0]

    germaniumdrivers.ensure_driver("firefox")

    firefox_capabilities = dict(webdriver.DesiredCapabilities.FIREFOX)
    firefox_capabilities['marionette'] = True

    return webdriver.Firefox(capabilities=firefox_capabilities,
                             timeout=timeout)


def _create_remote_firefox_capabilities_with_marionette(germanium, original_function):
    remote_capabilities = dict(webdriver.DesiredCapabilities.FIREFOX)
    remote_capabilities["marionette"] = True

    return remote_capabilities
