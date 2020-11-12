from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object


def parent_node_g(context, selector):
    germanium = find_germanium_object(context)
    element = _element(germanium, selector)

    return germanium.js("return arguments[0].parentNode;", element)
