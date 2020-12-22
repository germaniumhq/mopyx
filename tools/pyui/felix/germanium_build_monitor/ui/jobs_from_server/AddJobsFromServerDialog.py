from typing import List
from mopyx import render, action, render_call
import threading

from PySide2.QtWidgets import QDialog

from germanium_build_monitor.ui.generated.Ui_AddJobsFromServerDialog import Ui_Dialog

from germanium_build_monitor.model import RootModel
from germanium_build_monitor.model.JenkinsServer import JenkinsServer
from germanium_build_monitor.model.JenkinsMonitoredJob import JenkinsMonitoredJob
from germanium_build_monitor.model.JenkinsFolder import JenkinsFolder
from germanium_build_monitor.model.JenkinsJob import JenkinsJob
from germanium_build_monitor.model.Selection import Selection

from germanium_build_monitor.ui.WidgetSwitcher import WidgetSwitcher
from germanium_build_monitor.ui.LoadingFrame import LoadingFrame
from germanium_build_monitor.ui.ErrorFrame import ErrorFrame

from .SelectJobsFrame import SelectJobsFrame
from .load_data_from_server import load_server, ServerDialogModel


class AddJobsFromServerDialog(QDialog, Ui_Dialog):
    def __init__(self,
                 model: JenkinsServer,
                 main_window: QDialog,
                 edit_mode: bool = False,
                 ) -> None:
        super().__init__(main_window)

        self.model = ServerDialogModel(
            server=model,
            root_folder=JenkinsFolder(parent=None, name=f"All {model.name}"))

        self.setupUi(self)

        self.content = WidgetSwitcher(self.content_holder)

        self.wire_signals()
        self.update_from_model()
        self.reactive_update_from_model()
        self.load_content_from_server()

    def wire_signals(self):
        self.close_button.clicked.connect(self.close)
        self.select_button.clicked.connect(self.add_server_and_jobs)

    def update_from_model(self):
        self.server_name_label.setText(self.model.server.name)

    @action
    def add_server_and_jobs(self):
        server = self.model.server

        def find_selected_jobs(folder: JenkinsFolder) -> List[JenkinsJob]:
            result = []

            for sub_folder in folder.folders:
                if sub_folder.selected != Selection.UNSELECTED:
                    result.extend(find_selected_jobs(sub_folder))

            for job in folder.jobs:
                if job.selected == Selection.SELECTED:
                    result.append(job)

            return result

        selected_jobs = find_selected_jobs(self.model.root_folder)

        for job in selected_jobs:
            monitored_job = JenkinsMonitoredJob(
                name=job.name,
                full_name=job.full_name
            )
            server.monitored_jobs.append(monitored_job)

        RootModel.root_model.servers.append(server)

        self.close()

    @render
    def reactive_update_from_model(self):
        @render_call
        def select_button_enabled():
            enabled = self.model.loaded and self.model.root_folder.selected != Selection.UNSELECTED
            self.select_button.setEnabled(enabled)

        if self.model.error:
            self.content.set(ErrorFrame(self.model.error, self.load_content_from_server))
        elif not self.model.loaded:
            self.content.set(LoadingFrame())
        else:
            self.content.set(
                SelectJobsFrame(
                    self.model.server,
                    self.model.root_folder))

    def load_content_from_server(self):
        @action
        def clear_model():
            self.model.loaded = False
            self.model.error = None

        clear_model()

        threading.Thread(target=lambda: load_server(self.model)).start()

