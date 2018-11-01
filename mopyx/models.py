from typing import Any, Set, Dict, TypeVar, Callable, cast
import functools

import mopyx.rendering as rendering

T = TypeVar('T')
_update_index: int = 0


def action(f: Callable[..., T]) -> Callable[..., T]:
    """
    Do multiple operations on the model, at the end of which the
    rendering will be updated.
    """
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        global _update_index

        try:
            _update_index += 1
            return f(*args, **kw)
        finally:
            _update_index -= 1

            if _update_index == 0:
                rendering.call_registered_renderers()

    return wrapper


class ModelProxy(object):
    """
    Tracks who was rendered from what properties.
    """

    def __init__(self, target):
        self._mopyx_target = target
        self._mopyx_renderers: Dict[str, Set[rendering.RendererFunction]] = dict()

    def __getattr__(self, name: str):
        """
        Gets an attribute from the underlying object. In case there
        is an active renderer, it's registered as a dependency for
        this model property.
        """
        if rendering.active_renderers:
            renderers = self._mopyx_renderers.get(name, None)

            if not renderers:
                renderers = set()
                self._mopyx_renderers[name] = renderers

            renderer = rendering.active_renderers[-1]
            renderers.add(renderer)

            renderer.add_model_listener(self, name)

        return self._mopyx_target.__getattribute__(name)

    @action
    def __setattr__(self, name: str, value: Any):
        """
        Sets an attribute to the underlying object. Registered renderers
        will be called at the end of the root @action operation.
        """
        if name.startswith("_mopyx"):
            super().__setattr__(name, value)
            return

        setattr(self._mopyx_target, name, value)

        renderers = self._mopyx_renderers.get(name, None)
        if renderers:
            for renderer in renderers:
                rendering.register_render_refresh(renderer)

    def _mopyx_unregister(self, name, renderer):
        """
        Unregister a renderer from the given property.
        """
        self._mopyx_renderers[name].remove(renderer)


def model(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        result = f(*args, **kw)

        return cast(T, ModelProxy(result))

    return wrapper

