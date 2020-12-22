import functools
from typing import TypeVar, Callable, Optional, cast

from mopyx import rendering

T = TypeVar("T")

_update_index = 0


def action(f: Callable[..., T]) -> Callable[..., T]:
    """
    Do multiple operations on the model, at the end of which the
    rendering will be updated.
    """

    @functools.wraps(f)
    def action_wrapper(*args, **kw) -> Optional[T]:
        global _update_index

        if rendering.is_active_ignore_updates_renderer():
            return None

        try:
            _update_index += 1

            return f(*args, **kw)
        finally:
            _update_index -= 1

            if _update_index == 0:
                if rendering.is_debug_mode:
                    print(f"{rendering.indent()}action: {f}")

                rendering.call_registered_renderers()

    return cast(Callable[..., T], action_wrapper)
