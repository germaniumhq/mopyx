import functools
from typing import TypeVar, Callable

T = TypeVar("T")


class WearyContext:
    def __init__(self) -> None:
        super(WearyContext, self).__init__()


def _decorate_with_context(property_name: str, method_impl: Callable) -> Callable:
    """
    Normally a function for a property has only the `self`
    as an attribute. Since we want to also pass some context
    to that function, we wrap the call in this function that
    creates the context, and passes it. The `decorated_function`
    still has only `self` as an argument.

    :param property_name:
    :param method_impl:
    :return:
    """

    @functools.wraps(method_impl)
    def decorated_function(self):
        if property_name in self._data:
            return self._data[property_name]

        ctx = WearyContext()

        result = method_impl(self, ctx)
        self._data[property_name] = result

        return result

    return decorated_function
