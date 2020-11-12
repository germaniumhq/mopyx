

def _ensure_list(item):
    """
    Ensures that the given item is a list.
    :param item:
    :return:
    """
    if item is None:
        return []

    if isinstance(item, list):
        return item

    if isinstance(item, tuple):
        return list(item)

    return [item]
