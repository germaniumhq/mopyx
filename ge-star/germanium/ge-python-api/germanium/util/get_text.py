import re

from selenium.webdriver.remote.webelement import WebElement

from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object


def get_text_g(context, selector):
    germanium = find_germanium_object(context)

    if not selector:
        raise Exception("The passed selector was null for the get_text() call. "
                        "If you are using it in combination with waited() "
                        "(e.g. get_text(waited(...)), it means waited could "
                        "find the element.")

    if isinstance(selector, WebElement):
        element = selector
    else:
        element = _element(germanium, selector)

    result = germanium.js("return arguments[0].textContent || arguments[0].innerText || '';",
                          element)

    return re.sub("\r\n", "\n", str(result))
