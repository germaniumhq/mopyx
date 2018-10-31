from typing import Callable, TypeVar, List, Dict, Set, cast
import functools

T = TypeVar('T')


class RendererFunction:
    def __init__(self, f) -> None:
        self.callable = f


active_renderers: List[RendererFunction] = list()


def render(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        try:
            renderer = RendererFunction(f)
            active_renderers.append(renderer)
            return f(*args, **kw)
        finally:
            active_renderers.pop()

    return wrapper


class ModelProxy(object):
    """
    Tracks who was rendered from what properties.
    """

    def __init__(self, target):
        self._mopyx_target = target
        self._mopyx_renderers: Dict[str, Set[RendererFunction]] = dict()

    def __getattr__(self, name):
        if active_renderers:
            renderers = self._mopyx_renderers.get(name, None)

            if not renderers:
                renderers = set()
                self._mopyx_renderers[name] = renderers

            renderers.add(active_renderers[-1])

        return self._mopyx_target.__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith("_mopyx"):
            super().__setattr__(name, value)
            return

        setattr(self._mopyx_target, name, value)

        renderers = self._mopyx_renderers.get(name, None)
        if renderers:
            for renderer in renderers:
                renderer.callable()


def model(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        result = f(*args, **kw)

        return cast(T, ModelProxy(result))

    return wrapper


def render_call(f: Callable[..., T]) -> T:
    @render
    def internal_render():
        return f()

    return internal_render()

