from selenium import webdriver
from germanium.impl._workaround import workaround
from germanium.wa.firefox_open_browser_with_marionette import \
    _is_use_marionette_evironment_var_set, \
    _create_remote_firefox_capabilities_with_marionette


class GermaniumRemote(webdriver.Remote):
    def __init__(self, *args, **kw):
        super(GermaniumRemote, self).__init__(*args, **kw)

    def execute(self, driver_command, params=None):
        if driver_command != 'newSession':
            return super(GermaniumRemote, self).execute(driver_command, params=params)

        if params:
            params.pop('capabilities', None)

        return super(GermaniumRemote, self).execute(driver_command, params=params)


@workaround(_is_use_marionette_evironment_var_set,
            _create_remote_firefox_capabilities_with_marionette)
def _create_remote_firefox_capabilities():
    remote_capabilities = dict(webdriver.DesiredCapabilities.FIREFOX)
    remote_capabilities["marionette"] = False
    remote_capabilities["unexpectedAlertBehaviour"] = "ignore"

    return remote_capabilities
