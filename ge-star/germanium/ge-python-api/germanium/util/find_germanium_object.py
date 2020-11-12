from germanium.driver import GermaniumDriver
from germanium.impl import _ensure_list


def find_germanium_object(items):
    """
    Finds the germanium object in the given call. Searches it
    first in the parameter list, and if is not there, it searches
    it in the self reference, as either self.germanium or self._germanium.
    :param items:
    :return:
    """
    items = _ensure_list(items)

    for item in items:
        if isinstance(item, GermaniumDriver):
            return item

    self = items[0]  # get the self/context reference

    _germanium = getattr(self, "germanium", None)

    if _germanium:
        return _germanium

    return self._germanium
