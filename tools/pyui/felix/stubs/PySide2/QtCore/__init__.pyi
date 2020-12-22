from typing import Callable, Any, TypeVar

T = TypeVar('T')


class QEvent:
    def connect(self, callback: Callable[..., Any]) -> None:
        pass


class QTimer:
    def __init__(self, window) -> None:
        self.timeout = QEvent()

    def start(self, repeat_millis: int) -> None:
        pass

    def stop(self) -> None:
        pass


class QMetaObject:
    pass


class QObject:
    pass


class QSize:
    def __init__(self,
                 w: int,
                 h: int) -> None:
        pass


def Slot() -> Callable[..., Callable[..., T]]:
    pass
