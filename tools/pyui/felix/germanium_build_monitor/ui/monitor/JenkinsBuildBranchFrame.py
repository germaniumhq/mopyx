from mopyx import render_call, render
import arrow

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QSize

from germanium_build_monitor.ui.generated.Ui_JenkinsBuildBranchFrame import Ui_Form
from germanium_build_monitor.model.JenkinsJobBranch import JenkinsJobBranch
from germanium_build_monitor.resources.icons import aggregate_status_icon, get_icon
from germanium_build_monitor.ui.core import clear_layout
import webbrowser

from .SingleBuildStatusFrame import SingleBuildStatusFrame


class JenkinsBuildBranchFrame(QWidget, Ui_Form):
    def __init__(self, branch: JenkinsJobBranch) -> None:
        super().__init__()

        self.setupUi(self)

        self.project_name_button.setText(branch.project_name)
        self.branch_name_button.setText(branch.decoded_branch_name)

        def open_project():
            webbrowser.open(branch.parent_monitored_job.url)

        def open_branch():
            webbrowser.open(branch.url)

        self.project_name_button.clicked.connect(open_project)
        self.branch_name_button.clicked.connect(open_branch)

        self.ignore_branch_button.setIcon(get_icon("build_ignored.png"))
        self.ignore_branch_button.toggled.connect(branch.set_ignored)

        @render_call
        def update_status_icon() -> None:
            self.status_icon_label.setPixmap(aggregate_status_icon(branch).pixmap(QSize(32, 32)))

        @render_call
        def update_last_builds() -> None:
            clear_layout(self.previous_builds_container)

            for build in reversed(branch.last_builds):
                self.previous_builds_container.addWidget(SingleBuildStatusFrame(build))

        @render_call
        def update_time() -> None:
            if branch.last_build_timestamp is None:
                self.time_label.setText("<i>not run</i>")
                return

            time = arrow.get(branch.last_build_timestamp / 1000.0).humanize()
            self.time_label.setText(time)

        @render(ignore_updates=True)
        def update_ignore_branch_button():
            self.ignore_branch_button.setChecked(branch.is_ignored)

        update_ignore_branch_button()
