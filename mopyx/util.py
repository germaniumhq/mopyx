from typing import TypeVar, Iterable, Optional, Set
from mopyx import action

T = TypeVar("T")


@action
def merge_model(destination: T, source: T, already_processed: Optional[Set] = None) -> bool:
    if not already_processed:
        already_processed = set()

    try:
        if destination in already_processed:
            return True

        already_processed.add(source)  # destination is being mutated
    except Exception:
        pass  # we ignore unhashable items

    if isinstance(source, list):
        return merge_model_lists(destination, source, already_processed)

    if not is_mopyx_model(destination) or not is_mopyx_model(source):
        if destination == source:
            return True

        return False

    for prop in model_properties(destination):
        destination_value = getattr(destination, prop)
        source_value = getattr(source, prop)

        if isinstance(source_value, list):
            if merge_model_lists(destination_value, source_value, already_processed):
                continue

            setattr(destination, prop, source_value)
            continue

        if is_mopyx_model(source_value):
            if merge_model(destination_value, source_value, already_processed):
                continue

            setattr(destination, prop, source_value)
            continue

        if destination_value == source_value:
            continue

        setattr(destination, prop, source_value)

    return True


def merge_model_lists(destination, source, already_processed: Set) -> bool:
    if destination is None:
        return False

    if len(source) != len(destination):
        return False

    for i in range(len(source)):
        if not merge_model(destination[i], source[i], already_processed):
            destination[i] = source[i]
            continue

    return True


def model_properties(item: T) -> Iterable[str]:
    return item.__dict__.keys()


def is_mopyx_model(item) -> bool:
    try:
        if item._mopyx_renderers is not None:
            return True
        return False
    except Exception:
        return False
