from typing import TypeVar, Callable, Dict, Set, Any

from mopyx import rendering
from mopyx.computed_property import ComputedProperty
from mopyx.decorator_action import action
from mopyx.proxy_list import ListModelProxy

T = TypeVar("T")


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
