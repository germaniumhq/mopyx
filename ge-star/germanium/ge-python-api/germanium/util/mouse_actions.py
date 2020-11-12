from germanium.impl import ActionChains

from germanium.points import Point
from ._action_element_finder import _element
from .find_germanium_object import find_germanium_object


from germanium.impl._workaround import workaround
from germanium.wa.edge_move_to_element import \
    _is_microsoft_edge, _edge_move_to_element_with_offset
from germanium.wa.ie_eq_8_9_move_mouse_check_hover import \
    _is_older_ie_with_bugs_on_scroll, _ie_move_element_checking_scroll

def _element_or_position(germanium, selector):
    if isinstance(selector, Point):
        return selector
    return _element(germanium, selector)


def _element_or_none(germanium, selector, point):
    """
    Function to check if the given selector is only a regular
    element without offset clicking. If that is the case, then we
    enable the double hovering in the mouse actions, to solve a
    host of issues with hovering and scrolling, such as elements
    appearing on mouse in, or edge not hovering correctly.
    :param germanium:
    :param selector:
    :param point:
    :return:
    """
    if isinstance(selector, Point):
        return None

    if point:
        return None

    return _element(germanium, selector)


@workaround(_is_microsoft_edge, _edge_move_to_element_with_offset)
@workaround(_is_older_ie_with_bugs_on_scroll, _ie_move_element_checking_scroll)
def _move_to_element(germanium, action, element):
    action.move_to_element(element)


def _move_mouse(germanium, selector, point, move_mouse_over=False, action=None):
    if not action:
        action = ActionChains(germanium.web_driver)

    element = _element_or_position(germanium, selector)

    if isinstance(element, Point):
        action.move_to_element_with_offset(
            germanium.S('body').element(),
            element.x,
            element.y)
    elif selector and point:
        action.move_to_element_with_offset(
            element,
            point.x,
            point.y)
    elif move_mouse_over and selector:
        _move_to_element(germanium, action, element)

    return action


def click_g(context, selector=None, point=None, move_mouse_over=True):
    """ Click the given selector
    :param context:
    :param selector:
    :param point:
    :param move_mouse_over:
    """
    germanium = find_germanium_object(context)

    if move_mouse_over:
        element = _element_or_none(germanium, selector, point)

        if element:
            _move_mouse(germanium, element, None, move_mouse_over)\
                .click(on_element=element)\
                .perform()

            return

    _move_mouse(germanium, selector, point, move_mouse_over)\
        .click()\
        .perform()


def right_click_g(context, selector=None, point=None, move_mouse_over=True):
    """ Right click the given location
    :param context:
    :param selector:
    :param point:
    :param move_mouse_over:
    """
    germanium = find_germanium_object(context)

    if move_mouse_over:
        element = _element_or_none(germanium, selector, point)

        if element:
            _move_mouse(germanium, element, None, move_mouse_over) \
                .context_click(on_element=element) \
                .perform()

            return

    _move_mouse(germanium, selector, point, move_mouse_over) \
        .context_click() \
        .perform()


def double_click_g(context, selector=None, point=None, move_mouse_over=True):
    """ Double click the given location
    :param context:
    :param selector:
    :param point:
    :param move_mouse_over:
    """
    germanium = find_germanium_object(context)

    if move_mouse_over:
        element = _element_or_none(germanium, selector, point)

        if element:
            _move_mouse(germanium, element, None, move_mouse_over) \
                .double_click(on_element=element) \
                .perform()

            return

    _move_mouse(germanium, selector, point, move_mouse_over) \
        .double_click() \
        .perform()


def hover_g(context, selector=None, point=None):
    """ Hover the given location
    :param context:
    :param selector:
    :param point:
    """
    germanium = find_germanium_object(context)

    _move_mouse(germanium, selector, point, move_mouse_over=True) \
        .perform()
