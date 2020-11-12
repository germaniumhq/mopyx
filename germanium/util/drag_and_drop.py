from .find_germanium_object import find_germanium_object

from .mouse_actions import _move_mouse, _element_or_none


def drag_and_drop_g(context, from_selector, to_selector, from_point=None, to_point=None):
    germanium = find_germanium_object(context)

    from_element = _element_or_none(germanium, from_selector, from_point)

    if from_element:
        action = _move_mouse(germanium, from_element, point=None, move_mouse_over=True) \
            .click_and_hold(on_element=from_element)
    else:
        action = _move_mouse(germanium, from_selector, from_point, move_mouse_over=True) \
            .click_and_hold()

    to_element = _element_or_none(germanium, to_selector, to_point)

    if to_element:
        action = _move_mouse(germanium, to_element, point=None, move_mouse_over=True, action=action) \
            .release(on_element=to_element)
    else:
        action = _move_mouse(germanium, to_selector, to_point, move_mouse_over=True, action=action) \
            .release()

    action.perform()
