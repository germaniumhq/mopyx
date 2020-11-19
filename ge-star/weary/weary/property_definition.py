import types
from typing import Callable, TypeVar

from weary.context import _decorate_with_context
from weary.method_registrations import method_registrations

T = TypeVar("T")


def property(clazz, property_name) -> Callable[..., Callable[..., T]]:
    if not hasattr(clazz, "_weary_base"):
        raise Exception(
            "You can only override properties for classes decorated "
            "with `@weary.model`."
        )

    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        context_aware_function = _decorate_with_context(property_name, f)
        method_registrations[clazz._weary_base][property_name] = f
        property_definition = types.DynamicClassAttribute(
            context_aware_function, clazz._weary_base
        )
        setattr(
            clazz._weary_base,
            property_name,
            property_definition,
        )

        def set_value(self, value) -> None:
            self._data[property_name] = value

        property_definition.fset = set_value  # type: ignore

        return f

    return wrapper_builder
