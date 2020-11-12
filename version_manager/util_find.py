from typing import Callable, Iterable, TypeVar, Union


T = TypeVar("T")
N = Union[T, None]


def find(check: Callable[[T], bool], items: Iterable[T]) -> N:
    for item in items:
        if check(item):
            return item

    return None
