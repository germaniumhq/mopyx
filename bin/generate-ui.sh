cd $(readlink -f "$(dirname "$0")/..")

pyside2-uic ui/AddServerDialog.ui > germanium_build_monitor/ui/generated/Ui_AddServerDialog.py
pyside2-uic ui/AddJobsFromServer.ui > germanium_build_monitor/ui/generated/Ui_AddJobsFromServerDialog.py
pyside2-uic ui/MainDialog.ui > germanium_build_monitor/ui/generated/Ui_MainDialog.py
pyside2-uic ui/MainWindow.ui > germanium_build_monitor/ui/generated/Ui_MainWindow.py

pyside2-uic ui/NewStartFrame.ui > germanium_build_monitor/ui/generated/Ui_NewStartFrame.py
pyside2-uic ui/ServersOverviewFrame.ui > germanium_build_monitor/ui/generated/Ui_ServersOverviewFrame.py
pyside2-uic ui/SelectJobsFrame.ui > germanium_build_monitor/ui/generated/Ui_SelectJobsFrame.py
pyside2-uic ui/LoadingFrame.ui > germanium_build_monitor/ui/generated/Ui_LoadingFrame.py
pyside2-uic ui/ErrorFrame.ui > germanium_build_monitor/ui/generated/Ui_ErrorFrame.py

pyside2-uic ui/JenkinsServerFrame.ui > germanium_build_monitor/ui/generated/Ui_JenkinsServerFrame.py
pyside2-uic ui/LoadingJobFrame.ui > germanium_build_monitor/ui/generated/Ui_LoadingJobFrame.py
pyside2-uic ui/JenkinsBuildBranchFrame.ui > germanium_build_monitor/ui/generated/Ui_JenkinsBuildBranchFrame.py
pyside2-uic ui/SingleBuildStatusFrame.ui > germanium_build_monitor/ui/generated/Ui_SingleBuildStatusFrame.py

