from typing import Tuple, Any, Callable, Optional
import concurrent.futures


class ProcessPool:
    def __init__(self,
                 max_workers: int = 0,
                 max_tasks: int = 0,
                 initializer: Optional[Callable[..., Any]] = None,
                 initargs: Tuple = ()) -> None: ...

    def schedule(self,
                 function: Callable,
                 args=(),
                 kwargs={},
                 timeout=None) -> concurrent.futures.Future: ...

