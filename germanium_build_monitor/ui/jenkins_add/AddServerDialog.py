from typing import Optional

from mopyx import render_call, model
import traceback
import threading

from PySide2.QtWidgets import QDialog, QMessageBox, QFrame

from germanium_build_monitor.ui.core import ui_thread_call

from germanium_build_monitor.ui.generated.Ui_AddServerDialog import Ui_Dialog
from germanium_build_monitor.ui.WidgetSwitcher import WidgetSwitcher
from germanium_build_monitor.ui.LoadingFrame import LoadingFrame
from germanium_build_monitor.ui.ErrorFrame import Error

from germanium_build_monitor.model.JenkinsServer import JenkinsServer, jenkins_server

from germanium_build_monitor.actions import select_jobs_from_jenkins_server_dialog


def not_empty(s: str) -> bool:
    return bool(s and s.strip())


@model
class AddServerDialogModel:
    def __init__(self):
        self.loading = False


class AddServerDialog(QDialog, Ui_Dialog):
    def __init__(self,
                 model: JenkinsServer,
                 main_window: QDialog,
                 edit_mode: bool = False,
                 ) -> None:
        super().__init__(main_window)
        self.setupUi(self)

        self.model = model
        self.dialog_model = AddServerDialogModel()

        self.loading_content = WidgetSwitcher(self.loading_content_holder)
        self.edit_mode = edit_mode  # are we adding, or editing?

        self.update_labels()

        self.wire_signals()
        self.update_from_model()

    def update_labels(self):
        if not self.edit_mode:
            return

        self.add_button.hide()
        self.setWindowTitle("Edit server...")

    def wire_signals(self):
        self.name_edit.textEdited.connect(self.update_name)
        self.url_edit.textEdited.connect(self.update_url)
        self.auth_check_box.clicked.connect(self.update_auth_status)
        self.user_edit.textEdited.connect(self.update_user)
        self.password_edit.textEdited.connect(self.update_password)

        self.add_button.clicked.connect(self.add_server)
        self.test_server_button.clicked.connect(self.test_server)
        self.close_button.clicked.connect(self.hide)

    def update_name(self):
        self.model.name = self.name_edit.text()

    def update_url(self):
        self.model.url = self.url_edit.text()

    def update_auth_status(self):
        self.model.use_authentication = self.auth_check_box.isChecked()

    def update_user(self):
        self.model.user = self.user_edit.text()

    def update_password(self):
        self.model.password = self.password_edit.text()

    def update_from_model(self):
        @render_call
        def update_auth_status():
            self.user_edit.setEnabled(self.model.use_authentication)
            self.password_edit.setEnabled(self.model.use_authentication)
            self.user_label.setEnabled(self.model.use_authentication)
            self.password_label.setEnabled(self.model.use_authentication)

        @render_call
        def set_add_button_enabled():
            enabled = not_empty(self.model.name) and \
                not_empty(self.model.url) and \
                not self.dialog_model.loading
            self.add_button.setEnabled(enabled)

        @render_call
        def set_test_server_button_enabled():
            enabled = not_empty(self.model.url) and not self.dialog_model.loading
            self.test_server_button.setEnabled(enabled)

        @render_call
        def loading_bar():
            if self.dialog_model.loading:
                self.loading_content.set(LoadingFrame())
            else:
                self.loading_content.set(QFrame())

        # no need to be reactive from these ones
        self.name_edit.setText(self.model.name)
        self.url_edit.setText(self.model.url)
        self.auth_check_box.setChecked(self.model.use_authentication)
        self.user_edit.setText(self.model.user)
        self.password_edit.setText(self.model.password)

    def add_server(self):
        self.close()
        select_jobs_from_jenkins_server_dialog(self.model)

    def test_server(self):
        self.dialog_model.loading = True
        threading.Thread(target=self.invoke_test_server).start()

    def invoke_test_server(self):
        error: Optional[Error] = None
        result: Optional[str] = None

        try:
            server = jenkins_server(self.model)
            server.get_whoami()
            version = server.get_version()

            result = f"User {self.model.user} connected. Jenkins version {version}."

        except Exception as e:
            error = Error(self.tr("Error: ") + str(e), traceback.format_exc())

        @ui_thread_call
        def show_result():
            self.dialog_model.loading = False

            if error:
                error_message = QMessageBox()

                error_message.setWindowTitle(self.tr("Server Unavailable"))
                error_message.setText(error.name)
                error_message.setDetailedText(error.stack)
                error_message.setIcon(QMessageBox.Critical)

                error_message.exec_()
            else:
                QMessageBox.information(self, "Success", result)

