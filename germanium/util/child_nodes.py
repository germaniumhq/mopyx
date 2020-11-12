from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object
from germanium.impl._load_script import load_script


def child_nodes_g(context, selector, only_elements=True):
    germanium = find_germanium_object(context)
    element = _element(germanium, selector)

    code = load_script(__name__, 'child-nodes.min.js')

    return germanium.js(code, element, only_elements)
