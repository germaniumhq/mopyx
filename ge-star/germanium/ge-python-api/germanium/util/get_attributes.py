from selenium.webdriver.remote.webelement import WebElement

from .find_germanium_object import find_germanium_object
from germanium.impl._load_script import load_script


def get_attributes_g(context, selector, only_visible=True):
    """
    Return the attributes for the element that is obtained
    from the selector as a dictionary object.
    :param context:
    :param selector:
    :param only_visible:
    :return:
    """
    germanium = find_germanium_object(context)

    if isinstance(selector, WebElement):
        element = selector
    else:
        element = germanium.S(selector).element(only_visible=only_visible)

    if not element:
        raise Exception("Unable to find '%s' to get_attributes." % selector)

    code = load_script(__name__, 'get-attributes.min.js')

    return germanium.js(code, element)
