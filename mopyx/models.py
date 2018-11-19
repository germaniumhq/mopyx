from typing import Any, Set, Dict, TypeVar, Callable, List, Optional, cast
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


class ComputedProperty:
    def __init__(self):
        self.initial_render = True
        self.value = None


def computed(f: Callable[..., T]) -> T:
    """
    Add a computed property. A computed property only updates
    when one of the inner values changes. A computed property
    is not allowed to change the state of the object.
    """
    @property  # type: ignore
    @functools.wraps(f)
    def computed_wrapper(self) -> T:
        context = self._mopyx_get_computed_property(f.__name__)

        # @computed properties might get evaluated for the first time
        # when already inside a @render function.
        #
        # This is a problem since when the parent render refreshes,
        # the computed wrapper will be called again. Since
        # this is actually a forced rerender that should recreate the
        # render call, but not invoke the function again.

        # the renderer will never reload when called from a
        # different renderer
        @functools.wraps(f)
        def update_value():
            context.value = f(self)

            # @computed properties are allowed to be computed first during the rendering
            # since they should not have side effects. Because of that, they will
            # not fire the model change on the very first rendering, if we're already
            # in a rendering stage.
            if context.initial_render and rendering.renderers.is_rendering_in_progress:
                return

            self._mopyx_register_refresh(f.__name__)

        if context.initial_render:
            r = rendering.RendererFunction(
                parent=None,
                f=update_value,
                _mode=rendering.RenderMode.COMPUTE,
                ignore_updates=False)

            r.render()

            context.initial_render = False

        return context.value

    return computed_wrapper  # type: ignore


class ListModelProxy(list):
    """
    Tracks items in a list for changes. Whenver the list changes, triggers the
    parent model property as changed.
    """
    def __init__(self,
                 model,
                 property_name: str,
                 target: List) -> None:
        super().__init__(list(target))
        self._mopyx_model = model
        self._mopyx_property_name = property_name

    def __getitem__(self, i):
        self._mopyx_model._mopyx_register_active_renderers(self._mopyx_property_name)
        return super().__getitem__(i)

    def __getslice__(self, i, j):
        self._mopyx_model._mopyx_register_active_renderers(self._mopyx_property_name)
        return super().__getslice__(i, j)

    @action
    def __setitem__(self, *argv, **kw):
        result = super().__setitem__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __setslice__(self, *argv, **kw):
        result = super().__setslice__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __delitem__(self, *argv, **kw):
        result = super().__delitem__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __delslice__(self, *argv, **kw):
        result = super().__delslice__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def append(self, *argv, **kw):
        result = super().append(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def clear(self, *argv, **kw):
        current_len = len(self)

        result = super().clear(*argv, **kw)

        if current_len:
            self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def extend(self, *argv, **kw):
        result = super().extend(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def insert(self, *argv, **kw):
        result = super().insert(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def pop(self, *argv, **kw):
        result = super().pop(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def remove(self, *argv, **kw):
        result = super().remove(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def reverse(self, *argv, **kw):
        result = super().reverse(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def sort(self, *argv, **kw):
        result = super().sort(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result


def model(base: Callable[..., T]) -> Callable[..., T]:
    class ModelProxy(base):  # type: ignore
        """
        Tracks who was rendered from what properties.
        """

        def __init__(self, *argv, **kw):
            self._mopyx_renderers: Dict[str, Set[rendering.RendererFunction]] = dict()
            self._mopyx_computed: Dict[str, ComputedProperty] = dict()

            super().__init__(*argv, **kw)

        @property
        def __dict__(self):
            result = dict(super().__dict__)

            if "_mopyx_renderers" in result:
                del result["_mopyx_renderers"]

            if "_mopyx_computed" in result:
                del result["_mopyx_computed"]

            return result

        def __getattribute__(self, name: str):
            """
            Gets an attribute from the underlying object. In case there
            is an active renderer, it's registered as a dependency for
            this model property.
            """
            if name.startswith("_mopyx"):
                return super().__getattribute__(name)

            if name == "__class__" or name == "__iter__":
                return super().__getattribute__(name)

            self._mopyx_register_active_renderers(name)

            return super().__getattribute__(name)

        def _mopyx_register_active_renderers(self, name: str) -> None:
            if rendering.renderers.active:
                renderer = rendering.renderers.active[-1]

                self._mopyx_register_renderer(name, renderer)

        def _mopyx_register_renderer(self, name: str, renderer) -> None:
            renderers = self._mopyx_renderers.get(name, None)

            if not renderers:
                renderers = set()
                self._mopyx_renderers[name] = renderers

            if renderer not in renderers:
                renderers.add(renderer)

                renderer.add_model_listener(self, name)

        @action
        def __setattr__(self, name: str, value: Any):
            """
            Sets an attribute to the underlying object. Registered renderers
            will be called at the end of the root @action operation that started
            doing the updates.
            """
            if name.startswith("_mopyx"):
                super().__setattr__(name, value)
                return

            if isinstance(value, list):
                value = ListModelProxy(self, name, value)

            super().__setattr__(name, value)

            if rendering.is_debug_mode:
                print(f"{rendering.indent()}change: {self}.{name} = {value}")

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

        def _mopyx_get_computed_property(self, name: str) -> ComputedProperty:
            computed_property_context = self._mopyx_computed.get(name, None)

            if not computed_property_context:
                computed_property_context = ComputedProperty()
                self._mopyx_computed[name] = computed_property_context

            return computed_property_context

    return ModelProxy
