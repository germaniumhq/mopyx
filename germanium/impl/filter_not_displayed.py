from selenium.common.exceptions import StaleElementReferenceException

from ._load_script import load_script


def _filter_one_for_action(germanium, found_items):
    items = _filter_not_displayed(germanium,
                                  found_items,
                                  only_visible=True,
                                  throw_when_empty=True)
    return items[0]


def _filter_not_displayed(germanium,
                          found_items,
                          only_visible=True,
                          throw_when_empty=False):
    if not found_items:
        if throw_when_empty:
            raise_no_items_found_for_action()
        return list()

    if not only_visible:
        return found_items

    js_arguments = []

    code = load_script(__name__, 'filter-not-displayed.min.js')

    js_arguments.append(code)
    js_arguments.extend(found_items)

    try:
        result = germanium.js(*js_arguments)
    except StaleElementReferenceException:
        result = []

    if not result and throw_when_empty:
        raise_no_visible_items_found_for_action(found_items)

    return result


def raise_no_visible_items_found_for_action(found_items):
    raise Exception("While there were %d element(s) found, all of them were "
                    "either invisible (display: none, visibility: false, or "
                    "position off screen), or elements that are detached "
                    "from the current DOM document. Detached elements might "
                    "happen if the action is called while the page is "
                    "reloading." % len(found_items))


def raise_no_items_found_for_action():
    raise Exception("No items, visible or invisible, matched the selector given "
                    "for the action.")
