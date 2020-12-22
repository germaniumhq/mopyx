from mopyx import render
from PySide2.QtWidgets import QMainWindow

from germanium_build_monitor.ui.generated.Ui_MainWindow import Ui_MainWindow

from germanium_build_monitor.model import RootModel
from germanium_build_monitor.ui import help_show
from germanium_build_monitor.resources.icons import get_icon

main_window = None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.setWindowIcon(get_icon("favicon.ico"))
        self.setWindowTitle("Felix Build Monitor - master")

        self.content = WidgetSwitcher(self.current_view)

        self.minimize_action.triggered.connect(self.hide)
        self.exit_action.triggered.connect(exit_application)
        self.about_felix_action.triggered.connect(lambda: help_show.help_about(self))
        self.about_qt_action.triggered.connect(lambda: help_show.help_about_qt(self))

        self.update_current_view()

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

    @render
    def update_current_view(self):
        if not RootModel.root_model.servers:
            self.content.set(NewStartFrame())
        else:
            self.content.set(ServersOverviewFrame())

    @staticmethod
    def instance() -> 'MainWindow':
        global main_window

        if not main_window:
            main_window = MainWindow()
            main_window.show()

        return main_window


from .ServersOverviewFrame import ServersOverviewFrame
from .WidgetSwitcher import WidgetSwitcher
from .NewStartFrame import NewStartFrame

from germanium_build_monitor.actions import exit_application
