from typing import List, TypeVar, Callable, Set, Optional, Any, Tuple, Union
import functools

T = TypeVar('T')


active_renderers: List['RendererFunction'] = list()
registered_renderers: Set['RendererFunction'] = set()
is_rendering_in_progress = False


class RendererFunction:
    def __init__(self,
                 parent: Optional['RendererFunction'],
                 f: Callable[..., T],
                 ignore_updates: bool) -> None:
        self.parent = parent
        self.f = f
        self.dependents: List['RendererFunction'] = list()
        self._terminated = False
        self._models: Set[Tuple[Any, str]] = set()
        self.ignore_updates = ignore_updates
        self.args: Any = None
        self.kw: Any = None

        if parent:
            parent.dependents.append(self)

    def render(self) -> T:
        try:
            active_renderers.append(self)

            for dependent in self.dependents:
                dependent.unregister()

            self.dependents.clear()

            return self.f(*self.args, **self.kw)
        finally:
            active_renderers.pop()

    def _set_args_kw(self, *args, **kw):
        self.args = args
        self.kw = kw

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


def render(*r_args, **r_kw) -> Union[Callable[..., Callable[..., T]], Callable[..., T]]:
    """
    Calls the given renderer function, and registers the call for
    future use.
    """
    ignore_updates = False

    if 'ignore_updates' in r_kw:
        ignore_updates = r_kw['ignore_updates']

    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        parent = active_renderers[-1] if active_renderers else None
        renderer = RendererFunction(parent=parent,
                                    f=f,
                                    ignore_updates=ignore_updates)

        @functools.wraps(f)
        def wrapper(*args, **kw) -> T:
            renderer._set_args_kw(*args, **kw)

            return renderer.render()

        return wrapper

    if r_args:
        return wrapper_builder(r_args[0])

    return wrapper_builder


def render_call(f: Callable[..., T],
                ignore_updates: bool = False) -> T:
    @render(ignore_updates=ignore_updates)
    def internal_render():
        return f()

    return internal_render()


def register_render_refresh(renderer: RendererFunction):
    global is_rendering_in_progress

    if is_rendering_in_progress:
        if not active_renderers or not active_renderers[-1].ignore_updates:
            active_renderers_names = ", ".join(map(lambda it: str(it.f), active_renderers))
            raise Exception("Rendering is already in progress. Normally you shouldn't call actions inside rendering. "
                            "If you really know what you're doing you can explicitly ignore the model updates in "
                            "rendering (`@render(ignore_updates=True)`) to break circular dependencies. Renderer: "
                            f"{renderer.f}. Active renderers: {active_renderers_names}.")

        return  # we don't add the renderers, because we're ignoring updates

    registered_renderers.add(renderer)


def call_registered_renderers():
    global is_rendering_in_progress

    try:
        is_rendering_in_progress = True

        for renderer in list(registered_renderers):
            if renderer.has_parents(registered_renderers):
                registered_renderers.remove(renderer)
                continue

        registered_renderers_copy = registered_renderers.copy()
        registered_renderers.clear()

        for renderer in registered_renderers_copy:
            renderer.render()
    finally:
        is_rendering_in_progress = False

