from typing import List, TypeVar, Callable, Set, Optional, Any, Tuple
import functools

T = TypeVar('T')


active_renderers: List['RendererFunction'] = list()
registered_renderers: Set['RendererFunction'] = set()


class RendererFunction:
    def __init__(self,
                 parent: Optional['RendererFunction'],
                 f: Callable[..., T],
                 args,
                 kw) -> None:
        self.parent = parent
        self.f = f
        self.args = args
        self.kw = kw
        self.dependents: List['RendererFunction'] = list()
        self._terminated = False
        self._models: Set[Tuple[Any, str]] = set()

        if parent:
            parent.dependents.append(self)

    def render(self) -> T:
        for dependent in self.dependents:
            dependent.unregister()

        self.dependents.clear()

        return self.f(*self.args, **self.kw)

    def unregister(self):
        if self._terminated:
            return

        self._terminated = True

        for dependent in self.dependents:
            dependent.unregister()

        for model, property_name in self._models:
            model._mopyx_unregister(property_name, self)

    def add_model_listener(self, model: Any, property_name: str) -> None:
        self._models.add((model, property_name))

    def has_parents(self, parent_set: Set['RendererFunction']) -> bool:
        parent = self.parent

        while parent:
            if parent in parent_set:
                return True
            parent = parent.parent

        return False


def render(f: Callable[..., T]) -> Callable[..., T]:
    """
    Calls the given renderer function, and registers the call for
    future use.
    """
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        try:
            parent = active_renderers[-1] if active_renderers else None
            renderer = RendererFunction(parent=parent, f=f, args=args, kw=kw)

            active_renderers.append(renderer)

            return renderer.render()
        finally:
            active_renderers.pop()

    return wrapper


def render_call(f: Callable[..., T]) -> T:
    @render
    def internal_render():
        return f()

    return internal_render()


def register_render_refresh(renderer: RendererFunction):
    registered_renderers.add(renderer)


def call_registered_renderers():
    for renderer in list(registered_renderers):
        if renderer.has_parents(registered_renderers):
            registered_renderers.remove(renderer)
            continue

    for renderer in registered_renderers:
        renderer.render()

    registered_renderers.clear()

