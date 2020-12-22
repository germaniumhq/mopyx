import functools
from typing import TypeVar, Callable

from mopyx import rendering

T = TypeVar("T")


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
                ignore_updates=False,
            )

            r.render()

            context.initial_render = False

        return context.value

    return computed_wrapper  # type: ignore
