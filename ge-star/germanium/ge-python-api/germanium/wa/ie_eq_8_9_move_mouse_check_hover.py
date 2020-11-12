import time

# W/A for the case the scrolling inactivates the hover.
# We delay the hover with 200ms, and we check if the scrolling
# of the page was done. If yes, it means the current hover is
# invalid. We hover -1, -1 to the current element, then we try
# to hover the element again.


def _is_older_ie_with_bugs_on_scroll(germanium):
    capabilities = germanium.web_driver.capabilities

    if capabilities['browserName'] != 'internet explorer':
        return False

    if capabilities['version'] == '8':
        return True

    return False


def _ie_move_element_checking_scroll(germanium, original_function,
                                     fn_germanium, fn_action, fn_element, **kw):
    def get_scroll_xy():
        return germanium.js("return [document.documentElement.scrollTop, "
                            "document.documentElement.scrollLeft];")

    simple_map = dict()

    def store_scroll_location():
        simple_map['initial_scroll'] = get_scroll_xy()

    def rescroll_if_changed(action):
        current_scroll = get_scroll_xy()

        if simple_map['initial_scroll'] != current_scroll:
            action\
                .move_to_element_with_offset(fn_element, -1, -1)\
                .move_to_element(fn_element)

    fn_action\
        .add_action(store_scroll_location) \
        .move_to_element(fn_element)\
        .add_action(lambda: time.sleep(0.2)) \
        .add_dynamic_action(rescroll_if_changed)
