from typing import Union, Callable, TypeVar

T = TypeVar('T')


def render(*r_args, **r_kw) -> Union[Callable[..., Callable[..., T]], Callable[..., T]]:
    """
    Calls the given renderer function, and registers the call for
    future use.
    """
    pass


def render_call(f: Callable[..., T],
                ignore_updates: bool = False) -> T:
    pass


def action(f: Callable[..., T]) -> Callable[..., T]:
    pass


def model(base: Callable[..., T]) -> Callable[..., T]:
    pass


def computed(prop: Callable[..., T]) -> T:
    pass
