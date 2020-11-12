from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object

from selenium.webdriver.support.select import Select


def get_value_g(context, selector):
    germanium = find_germanium_object(context)
    element = _element(germanium, selector)

    if element.tag_name == "select":
        multi = element.get_attribute("multiple")
        if multi and multi != "false":
            return list(map(lambda x: x.get_attribute("value"),
                            Select(element).all_selected_options))

    return germanium.js("return arguments[0].value;", element)
