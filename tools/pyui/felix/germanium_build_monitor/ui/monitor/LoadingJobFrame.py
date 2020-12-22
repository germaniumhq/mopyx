from PySide2.QtWidgets import QWidget

from germanium_build_monitor.ui.generated.Ui_LoadingJobFrame import Ui_Form
from germanium_build_monitor.ui.LoadingFrame import LoadingFrame

from germanium_build_monitor.model.JenkinsMonitoredJob import JenkinsMonitoredJob


class LoadingJobFrame(QWidget, Ui_Form):
    def __init__(self,
                 job: JenkinsMonitoredJob) -> None:
        super().__init__()

        self.setupUi(self)
        self.job_name_label.setText(job.name)
        self.content.addWidget(LoadingFrame())
