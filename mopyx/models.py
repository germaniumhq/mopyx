from typing import Any, Set, Dict, TypeVar, Callable, cast, List
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


class ListModelProxy(list):
    """
    Tracks items in a list for changes. Whenver the list changes, triggers the
    parent model property as changed.
    """
    def __init__(self,
                 model: 'ModelProxy',
                 property_name: str,
                 target: List) -> None:
        super().__init__(target)
        self._mopyx_model = model
        self._mopyx_property_name = property_name

    def __getitem__(self, i):
        return super().__getitem__(i)

    def __getslice__(self, i, j):
        return super().__getslice__(i, j)

    @action
    def __setitem__(self, i, y):
        result = super().__setitem__(self, i, y)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def __setslice__(self, i, j):
        result = super().__setslice__(self, i, j)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def __delitem__(self, i):
        result = super().__delitem__(self, i)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def __delslice__(self, i, j):
        result = super().__delslice__(self, i, j)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def append(self, *argv, **kw):
        result = super().append(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def clear(self, *argv, **kw):
        result = super().clear(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def extend(self, *argv, **kw):
        result = super().extend(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def insert(self, *argv, **kw):
        result = super().insert(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def pop(self, *argv, **kw):
        result = super().pop(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def remove(self, *argv, **kw):
        result = super().remove(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def reverse(self, *argv, **kw):
        result = super().reverse(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result

    @action
    def sort(self, *argv, **kw):
        result = super().sort(*argv, **kw)
        self._mopyx_model._mopix_register_refresh(self._mopyx_property_name)
        return result


class ModelProxy:
    """
    Tracks who was rendered from what properties.
    """

    def __init__(self, target):
        self._mopyx_target = target
        self._mopyx_renderers: Dict[str, Set[rendering.RendererFunction]] = dict()

        for key in dir(target):
            value = getattr(target, key)
            if isinstance(value, list):
                target.__setattr__(key, ListModelProxy(self, key, value))

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

        if isinstance(value, list):
            value = ListModelProxy(self, name, value)

        setattr(self._mopyx_target, name, value)
        self._mopyx_register_refresh(name)

    def _mopyx_register_refresh(self, name):
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

