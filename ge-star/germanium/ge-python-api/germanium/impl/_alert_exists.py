from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

from germanium.wa.firefox_without_marionette_alert import _is_firefox_without_marionette, _get_alert_firefox
from ._workaround import workaround


@workaround(_is_firefox_without_marionette, _get_alert_firefox)
def _get_alert(germanium):
    try:
        alert = germanium.web_driver.switch_to.alert
        alert.text

        germanium._last_alert = alert

        return alert
    except NoAlertPresentException:
        return germanium._last_alert


def allow_alert(germanium):
    """
    Marks a section of code as runnable even if there is an alert
    displayed. The section will return a reference to the alert
    itself if raised, from the given germanium instance.

    :param germanium:
    :return:
    """
    def decorator(code):
        def wrapper():
            try:
                return code()
            except UnexpectedAlertPresentException:
                pass
            except WebDriverException as e:
                if 'unexpected alert open' not in e.msg\
                        and 'COM method IWebBrowser2::Navigate2()' not in e.msg:
                    raise e
                print("An unexpected alert exception was caught by Germanium "
                      "while loading the page: %s" % e)

            return germanium.web_driver.switch_to.alert

        return wrapper

    return decorator