from typing import Callable
from PySide2.QtWidgets import QWidget

from germanium_build_monitor.ui.generated.Ui_ErrorFrame import Ui_Form


class Error:
    def __init__(self,
                 name: str,
                 stack: str) -> None:
        self.name = name
        self.stack = stack


class ErrorFrame(QWidget, Ui_Form):
    def __init__(self, error: Error, retry: Callable) -> None:
        super().__init__()

        self.setupUi(self)

        self.error_name_label.setText(error.name)
        self.error_stack_edit.setPlainText(error.stack)

        self.retry_button.clicked.connect(retry)

