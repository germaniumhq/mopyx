from mopyx import render_call, action
from mopyx.util import merge_model

import sys
import traceback
import threading
import time
import webbrowser

from PySide2.QtWidgets import QMenu

from germanium_build_monitor.ui.MainWindow import MainWindow
from germanium_build_monitor.ui.core import \
    create_qt_application, \
    create_qt_tray_icon, \
    show_notification, \
    ui_thread

from germanium_build_monitor.model import RootModel
from germanium_build_monitor.model import Settings
from germanium_build_monitor.model import persistence

from germanium_build_monitor.model.BuildStatus import BuildStatus
from germanium_build_monitor.model.SystrayItem import SystrayItem
from germanium_build_monitor.model.JenkinsServer import JenkinsServer, jenkins_server

from germanium_build_monitor.model.jenkins.remote.read_build_jobs import read_build_job_branches
from germanium_build_monitor.model.jenkins.operations import compare_branches

from germanium_build_monitor.actions import exit_application, monitoring_threads

import germanium_build_monitor.resources.icons as icons
from PySide2.QtWidgets import QMessageBox


class JobMonitorThread(threading.Thread):
    def __init__(self,
                 server: JenkinsServer):
        super().__init__()
        self.server = server
        self.error_shown = False

    def run(self) -> None:
        print(f"Server {self.server.name} is being monitored")

        @ui_thread
        @action
        def update_failed_count(job, successful: bool) -> None:
            if successful:
                job.failed_count = 0
                return

            job.failed_count += 1

            if job.failed_count < Settings.settings.maximum_failed_count:
                return

            if self.error_shown:
                return

            self.error_shown = True

            QMessageBox.critical(
                MainWindow.instance(),
                f"Failure monitoring {job.name}",
                f"Failure monitoring {job.name} on {self.server.name} "
                f"at {self.server.url}, after {job.failed_count} tries. "
                "Felix will now exit.")

            exit_application()

        @ui_thread
        @action
        def update_results(job, result) -> None:
            updated_branches = read_build_job_branches(job, result)

            try:
                if job.branches is None:
                    job.branches = updated_branches
                    return

                notifications = compare_branches(job.branches, updated_branches)

                if not merge_model(job.branches, updated_branches):
                    job.branches = updated_branches

                for notification in notifications:
                    if notification.branch.status == BuildStatus.IGNORED:
                        continue

                    icon = icons.build_status_icon(notification.branch.status)

                    show_notification(
                        notification.branch.project_name,
                        notification.branch.decoded_branch_name,
                        icon,
                        Settings.settings.notification_display_time * 1000
                    )

                    key = f"{notification.branch.project_name} "\
                          f"({notification.branch.decoded_branch_name}) "
                    systray_item = SystrayItem(
                        key,
                        notification.branch.status,
                        f"{key}{notification.build.name}",
                        lambda: webbrowser.open(notification.build.url)
                    )

                    RootModel.root_model.systray.add_request(systray_item)

                RootModel.root_model.systray.flush_requests()

                update_failed_count(job, True)
            except Exception:  # UI Exception
                traceback.print_exc()
                update_failed_count(job, False)

        while self.server in monitoring_threads:
            for job in self.server.monitored_jobs:
                try:
                    print(f"scanning: {job.name}")
                    result = jenkins_server(self.server).get_job_info(job.full_name, depth="2")

                except Exception:
                    update_failed_count(job, False)
                else:
                    update_results(job, result)

            time.sleep(10)
        print(f"Stopped monitoring {self.server.name}")


menu = None


def main() -> None:
    RootModel.root_model, Settings.settings = persistence.load_state()

    app = create_qt_application()
    tray_icon = create_qt_tray_icon()

    @render_call
    def update_systray_icon():
        # FIXME: this should check if there are builds available
        # and show the unknown status/main application icon.
        icon = icons.aggregate_status_icon(RootModel.root_model)

        if not icon:
            icon = icons.get_icon("favicon.ico")

        tray_icon.setIcon(icon)

    tray_icon.show()

    menu = QMenu()

    # We need to create the instance outside so it gets its own renderer
    MainWindow.instance()

    def show_main_window() -> None:
        MainWindow.instance().show()
        MainWindow.instance().activateWindow()

    @render_call
    def render_context_menu():
        menu.clear()
        menu.addAction(icons.get_icon("favicon.ico"), "Main Window") \
            .triggered.connect(show_main_window)

        if RootModel.root_model.systray.items:
            menu.addSeparator()

            for systray_item in RootModel.root_model.systray.items:
                icon = icons.build_status_icon(systray_item.status)

                menu.addAction(icon, systray_item.text)\
                    .triggered.connect(systray_item.action)

        menu.addSeparator()
        menu.addAction("Exit")\
            .triggered.connect(exit_application)

    tray_icon.setContextMenu(menu)

    @render_call
    def start_monitoring_threads():
        for server in RootModel.root_model.servers:
            if server in monitoring_threads:
                return

            thread = JobMonitorThread(server)
            monitoring_threads[server] = thread
            thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
