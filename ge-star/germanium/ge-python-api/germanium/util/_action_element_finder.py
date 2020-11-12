from germanium.impl import _filter_one_for_action


def _element(germanium, selector):
    """
    Finds a single element for doing a visual action.
    :param germanium:
    :param selector:
    :return:
    """
    element = None

    if selector:
        items = germanium.S(selector).element_list(only_visible=False)
        element = _filter_one_for_action(germanium, items)

    return element
