from selenium.webdriver.remote.webelement import WebElement

from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object
from germanium.impl._load_script import load_script


def get_style_g(context, selector, name):
    germanium = find_germanium_object(context)

    # FIXME: get styles from hidden attributes, see get_attributes
    if isinstance(selector, WebElement):
        element = selector
    else:
        element = _element(germanium, selector)

    code = load_script(__name__, 'get-style.min.js')

    return germanium.js(code, element, name)
