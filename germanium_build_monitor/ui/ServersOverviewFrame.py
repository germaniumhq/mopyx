from mopyx import render
from PySide2.QtWidgets import QWidget

from germanium_build_monitor.ui.generated.Ui_ServersOverviewFrame import Ui_Form
from germanium_build_monitor.ui.monitor.JenkinsServerFrame import JenkinsServerFrame
from germanium_build_monitor.model import RootModel
from germanium_build_monitor.ui.core import clear_layout


class ServersOverviewFrame(QWidget, Ui_Form):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)

        self.search_line_edit.textChanged.connect(self.update_model)

        self.set_search_text_from_model()
        self.load_from_model()

    def update_model(self, text):
        RootModel.root_model.search_text = text

    @render(ignore_updates=True)
    def set_search_text_from_model(self):
        self.search_line_edit.setText(RootModel.root_model.search_text)

    @render
    def load_from_model(self):
        clear_layout(self.content)

        for server in RootModel.root_model.servers:
            self.content.addWidget(JenkinsServerFrame(server))
