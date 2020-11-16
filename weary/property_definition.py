import types
from typing import Callable, TypeVar

from weary.method_registrations import method_registrations

T = TypeVar("T")


def property(clazz, function_name) -> Callable[..., Callable[..., T]]:
    if not hasattr(clazz, "_weary_base"):
        raise Exception("You can only override properties for classes decorated "
                        "with `@weary.model`.")

    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        method_registrations[clazz._weary_base][function_name] = f
        setattr(clazz._weary_base, function_name, types.DynamicClassAttribute(f, clazz._weary_base))
        return f

    return wrapper_builder
