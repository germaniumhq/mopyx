import functools
from typing import TypeVar, Type, Callable

from weary.method_registrations import method_registrations

T = TypeVar("T")


def model(f: Type[T]) -> Callable[..., T]:
    method_registrations[f] = dict()

    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return _create(f, *args, **kw)

    wrapper._weary_base = f  # type: ignore

    return wrapper


def _create(t: Type[T], *args, **kw) -> T:
    """
    Create the instance with the given type
    :param t:
    :return:
    """
    result = t()  # type: ignore
    result._data = dict()  # type: ignore

    if t not in method_registrations:
        raise Exception(f"{t} was not registered with @weary.model")

    for property_name, property_value in kw.items():
        if not hasattr(result, property_name):
            raise Exception(
                f"{property_name} is not defined on the @weary.model " f"class."
            )
        setattr(result, property_name, property_value)

    return result
