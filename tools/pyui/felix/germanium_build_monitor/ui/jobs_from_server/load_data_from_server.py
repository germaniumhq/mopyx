from typing import Optional

from mopyx import model
import traceback

from germanium_build_monitor.model.JenkinsServer import JenkinsServer, jenkins_server
from germanium_build_monitor.model.JenkinsFolder import JenkinsFolder

from germanium_build_monitor.model.jenkins.remote.read_job_tree import process

from germanium_build_monitor.ui.core import ui_thread_call
from germanium_build_monitor.ui.ErrorFrame import Error


@model
class ServerDialogModel:
    def __init__(self,
                 server: JenkinsServer,
                 root_folder: JenkinsFolder):
        self.server: JenkinsServer = server
        self.root_folder: JenkinsFolder = root_folder
        self.loaded = False
        self.error: Optional[Error] = None


def load_server(model: ServerDialogModel):
    server = model.server
    root_folder = model.root_folder

    error = None

    try:
        jenkins_api = jenkins_server(server)
        result = jenkins_api.get_all_jobs()
    except Exception as e:
        error = Error(str(e), traceback.format_exc())

    @ui_thread_call
    def update_model():
        if error:
            model.error = error
            return

        process(root_folder, result)

        model.loaded = True

