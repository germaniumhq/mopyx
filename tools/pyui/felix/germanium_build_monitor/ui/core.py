from typing import Callable, TypeVar

import functools
import sys
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QLayout
from PySide2.QtCore import QMetaObject, QObject, Qt, Slot
from PySide2.QtGui import QIcon
from queue import Queue

app = None
tray_icon = None

T = TypeVar('T')


def create_qt_application() -> QApplication:
    global app

    if not app:
        app = QApplication(sys.argv)

    return app


def create_qt_tray_icon() -> QSystemTrayIcon:
    global tray_icon

    if not tray_icon:
        tray_icon = QSystemTrayIcon()

    return tray_icon


class Invoker(QObject):
    def __init__(self):
        super(Invoker, self).__init__()
        self.queue = Queue()

    def invoke(self, func, *args):
        self.queue.put(lambda: func(*args))
        QMetaObject.invokeMethod(self, "handler", Qt.QueuedConnection)

    @Slot()
    def handler(self):
        f = self.queue.get()
        f()


invoker = Invoker()


def ui_thread_call(f: Callable[..., T]) -> Callable[..., T]:
    """
    Will call the given function on the PySide UI Thread.
    """
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return invoker.invoke(f, *args, **kw)

    return wrapper()


def ui_thread(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return invoker.invoke(f, *args, **kw)

    return wrapper


def show_notification(title: str,
                      message: str,
                      icon: QIcon,
                      delay: int = 4000) -> None:
    global tray_icon
    assert tray_icon
    tray_icon.showMessage(title, message, icon, delay)


def clear_layout(layout: QLayout) -> None:
    while True:
        layout_item = layout.takeAt(0)
        if not layout_item:
            break

        layout_item.widget().deleteLater()


def _(callable: Callable[..., T]) -> Callable[[], T]:
    """
    Make a new callable that ignores all its parameters, and just calls the
    given callable.
    :param callable:
    :return:
    """
    def ignore_args(*args, **kw):
        return callable()

    return ignore_args

