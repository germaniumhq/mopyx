from typing import Dict, Any
import sys

from germanium_build_monitor.model.JenkinsServer import JenkinsServer
from germanium_build_monitor.model import RootModel
from germanium_build_monitor.model import Settings
from germanium_build_monitor.model import persistence


def open_create_jenkins_server_dialog():
    """ Open the add server dialog. """
    main_dialog = MainWindow.instance()

    AddServerDialog(
        JenkinsServer(
            name="localhost",
            url="http://localhost:8080/",
            use_authentication=False,
            user="",
            password=""
        ),
        main_window=main_dialog,
        edit_mode=False,
    ).show()


def select_jobs_from_jenkins_server_dialog(server: JenkinsServer):
    main_dialog = MainWindow.instance()

    AddJobsFromServerDialog(
        server,
        main_window=main_dialog,
        edit_mode=False,
    ).show()


# FIXME not sure if this is the best place where they should live. Model?
monitoring_threads: Dict[JenkinsServer, Any] = dict()


def exit_application() -> None:
    monitoring_threads.clear()
    persistence.persist_state(RootModel.root_model, Settings.settings)
    sys.exit(0)


from germanium_build_monitor.ui.jenkins_add.AddServerDialog import AddServerDialog
from germanium_build_monitor.ui.jobs_from_server.AddJobsFromServerDialog import AddJobsFromServerDialog
from germanium_build_monitor.ui.MainWindow import MainWindow

