from selenium.common.exceptions import UnexpectedAlertPresentException


def _is_firefox_without_marionette(germanium):
    capabilities = germanium.web_driver.capabilities
    return capabilities['browserName'].lower() == 'firefox' and \
           ('marionette' not in capabilities or not capabilities['marionette'])


def _get_alert_firefox(germanium, original_function, *args, **kw):
    try:
        germanium.web_driver.execute_script("1 == 1")
        return germanium._last_alert
    except UnexpectedAlertPresentException as e:
        return germanium.web_driver.switch_to.alert
