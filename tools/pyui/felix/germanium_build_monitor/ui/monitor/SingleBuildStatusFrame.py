from mopyx import render_call
import webbrowser

from PySide2.QtWidgets import QWidget

from germanium_build_monitor.ui.generated.Ui_SingleBuildStatusFrame import Ui_Form

from germanium_build_monitor.model.JenkinsJobBranchBuild import JenkinsJobBranchBuild
from germanium_build_monitor.resources.icons import build_status_icon


class SingleBuildStatusFrame(QWidget, Ui_Form):
    def __init__(self,
                 build: JenkinsJobBranchBuild) -> None:
        super().__init__()

        self.build: JenkinsJobBranchBuild = build

        self.setupUi(self)

        self.icon.clicked.connect(self.open_build)

        @render_call
        def update_label():
            self.icon.setIcon(build_status_icon(self.build.status))
            self.icon.setToolTip(self.build.name)

    def open_build(self) -> None:
        webbrowser.open(self.build.url)

