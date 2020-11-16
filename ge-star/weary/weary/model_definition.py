import functools
from typing import TypeVar, Type, Callable

from weary.method_registrations import method_registrations

T = TypeVar("T")


class WearyContext:
    def __init__(self) -> None:
        pass


def model(f: Callable[..., T]) -> Callable[..., T]:
    method_registrations[f] = dict()

    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return _create(f, *args, **kw)

    wrapper._weary_base = f

    return wrapper


def _create(t: Type[T], *args, **kw) -> T:
    """
    Create the instance with the given type
    :param t:
    :return:
    """
    result = t(*args, **kw)

    if t not in method_registrations:
        raise Exception(f"{t} was not registered with @weary.model")

    for method_name, method_impl in method_registrations[t].items():
        setattr(result, method_name, _context_provider(result, method_impl))

    return result


def _context_provider(this, method_impl: Callable) -> Callable:
    def result():
        context = WearyContext()
        return method_impl(this, context)

    return result
