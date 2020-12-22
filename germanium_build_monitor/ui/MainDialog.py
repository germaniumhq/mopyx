from PySide2.QtWidgets import QDialog
from mopyx import render

from germanium_build_monitor.ui.generated.Ui_MainDialog import Ui_Dialog

from germanium_build_monitor.model import RootModel

main_dialog = None


class MainDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

        self.setupUi(self)

        self.content = WidgetSwitcher(self.current_view)

        self.update_current_view()

    @render
    def update_current_view(self):
        if not RootModel.root_model.servers:
            self.content.set(NewStartFrame())
        else:
            self.content.set(ServersOverviewFrame())

    @staticmethod
    def instance() -> 'MainDialog':
        global main_dialog

        if not main_dialog:
            main_dialog = MainDialog()
            main_dialog.show()

        return main_dialog


from .ServersOverviewFrame import ServersOverviewFrame
from .WidgetSwitcher import WidgetSwitcher
from .NewStartFrame import NewStartFrame

