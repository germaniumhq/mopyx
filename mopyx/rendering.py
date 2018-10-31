from typing import List, TypeVar, Callable, Set, Optional
import functools

T = TypeVar('T')


active_renderers: List['RendererFunction'] = list()
registered_renderers: Set['RendererFunction'] = set()


class RendererFunction:
    def __init__(self,
                 parent: Optional['RendererFunction'],
                 f: Callable[..., None],
                 args,
                 kw) -> None:
        self.parent = parent
        self.f = f
        self.args = args
        self.kw = kw
        #self.dependents: List['RendererFunction'] = set()

    def render(self):
        #for dependent in self.dependents:
        #    dependent.unregister()
        #self.dependents.clear()

        return self.f(*self.args, **self.kw)


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
    for renderer in registered_renderers:
        renderer.render()

    registered_renderers.clear()

