from typing import List, TypeVar, Callable, Set, Optional, Any, Tuple, Union, Dict
from enum import Enum
import functools
import os
import threading

T = TypeVar('T')


class RenderMode(Enum):
    RENDER: str = "render"
    COMPUTE: str = "compute"


class Renderers(threading.local):
    def __init__(self):
        self.active: List['RendererFunction'] = list()
        self.registered: Dict[RenderMode, Set['RendererFunction']] = dict()

        self.registered[RenderMode.RENDER] = set()
        self.registered[RenderMode.COMPUTE] = set()
        self.is_rendering_in_progress: Optional[RenderMode] = None


is_debug_mode = 'MOPYX_DEBUG' in os.environ
is_render_thread_check = 'MOPYX_THREAD_CHECK' in os.environ

thread_id: Optional[int] = None
renderers = Renderers()


def indent():
    return "  " * len(renderers.active)


class RendererFunction:
    def __init__(self,
                 parent: Optional['RendererFunction'],
                 f: Callable[..., T],
                 _mode: RenderMode,
                 ignore_updates: bool) -> None:
        self.parent = parent
        self.f = f
        self.dependents: List['RendererFunction'] = list()
        self._terminated = False
        self._models: Set[Tuple[Any, str]] = set()
        self._mode: RenderMode = _mode
        self.ignore_updates = ignore_updates
        self.args: Any = None
        self.kw: Any = None

        if parent:
            parent.dependents.append(self)

    def render(self) -> T:
        global thread_id

        try:
            if is_debug_mode:
                print(f"{indent()}renderer: {self} ({self.f})")

            renderers.active.append(self)

            if is_render_thread_check:
                if thread_id is None:
                    thread_id = threading.get_ident()
                elif thread_id != threading.get_ident():
                    raise Exception(f"Render thread id: {thread_id}, current thread id: {threading.get_ident()}")

            for dependent in self.dependents:
                dependent.unregister()

            self.dependents.clear()

            if self.args is not None and self.kw is not None:
                return self.f(*self.args, **self.kw)
            else:
                return self.f()
        finally:
            renderers.active.pop()

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
        if is_debug_mode:
            print(f"{indent()}model: {model}.{property_name}")

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
    _mode = RenderMode.RENDER

    if 'ignore_updates' in r_kw:
        ignore_updates = r_kw['ignore_updates']

    if '_mode' in r_kw:
        _mode = r_kw['_mode']

    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def render_wrapper(*args, **kw) -> T:
            parent = renderers.active[-1] if renderers.active else None
            renderer = RendererFunction(parent=parent,
                                        f=f,
                                        _mode=_mode,
                                        ignore_updates=ignore_updates)

            renderer._set_args_kw(*args, **kw)

            return renderer.render()

        return render_wrapper

    if r_args:
        return wrapper_builder(r_args[0])

    return wrapper_builder


def render_call(f: Callable[..., T],
                _mode: RenderMode = RenderMode.RENDER,
                ignore_updates: bool = False) -> T:
    @render(ignore_updates=ignore_updates, _mode=_mode)
    @functools.wraps(f)
    def render_call_internal_render():
        return f()

    return render_call_internal_render()


def register_render_refresh(renderer: RendererFunction):
    if renderers.is_rendering_in_progress == RenderMode.RENDER and renderer._mode == RenderMode.RENDER:
        if not is_active_ignore_updates_renderer():
            active_renderers_names = ", ".join(map(lambda it: str(it.f), renderers.active))
            raise Exception("Rendering is already in progress. Normally you shouldn't call actions inside rendering. "
                            "If you really know what you're doing you can explicitly ignore the model updates in "
                            "rendering (`@render(ignore_updates=True)`) to break circular dependencies. Renderer: "
                            f"{renderer.f}. Active renderers: {active_renderers_names}.")

        return  # we don't add the renderers, because we're ignoring updates

    renderers.registered[renderer._mode].add(renderer)


def call_registered_renderers():
    try:
        renderers.is_rendering_in_progress = RenderMode.COMPUTE

        for i in range(1000):
            if not renderers.registered[RenderMode.COMPUTE]:
                break

            for compute_renderer in clean_renderers(RenderMode.COMPUTE):
                compute_renderer.render()

        if renderers.registered[RenderMode.COMPUTE]:
            raise Exception("After iterating 1000 times, we still have registered renderers for @computed "
                            "values. Assuming an infinite loop.")

        renderers.is_rendering_in_progress = RenderMode.RENDER

        for renderer in clean_renderers(RenderMode.RENDER):
            renderer.render()
    finally:
        renderers.is_rendering_in_progress = None


def is_active_ignore_updates_renderer() -> bool:
    if not renderers.active:
        return False

    for renderer in renderers.active:
        if renderer.ignore_updates:
            return True

    return False


def clean_renderers(render_mode: RenderMode):
    registered = renderers.registered[render_mode]
    for renderer in list(registered):
        if renderer.has_parents(registered):
            registered.remove(renderer)
            continue

    renderers_copy = registered.copy()
    registered.clear()

    return renderers_copy

