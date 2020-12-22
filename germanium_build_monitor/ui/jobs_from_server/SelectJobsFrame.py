from typing import Any, Union, Optional
from mopyx import render, action
import itertools

from PySide2.QtWidgets import QWidget

from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtCore import Qt

from germanium_build_monitor.ui.generated.Ui_SelectJobsFrame import Ui_Form
from germanium_build_monitor.resources.icons import get_icon

from germanium_build_monitor.model.JenkinsServer import JenkinsServer
from germanium_build_monitor.model.JenkinsFolder import JenkinsFolder, Selection
from germanium_build_monitor.model.JenkinsJob import JenkinsJob


def as_qt_selection(value: Selection):
    if value == Selection.UNSELECTED:
        return Qt.CheckState.Unchecked
    elif value == Selection.SELECTED:
        return Qt.CheckState.Checked
    elif value == Selection.PARTIAL:
        return Qt.CheckState.PartiallyChecked
    else:
        raise Exception(f"Unknown enum value for selection {value}")


def as_selection(value: 'Qt.CheckState'):
    if value == Qt.CheckState.Checked:
        return Selection.SELECTED
    elif value == Qt.CheckState.Unchecked:
        return Selection.UNSELECTED
    else:
        return Selection.PARTIAL


class SelectJobsFrame(QWidget, Ui_Form):
    def __init__(self,
                 server: JenkinsServer,
                 root: JenkinsFolder) -> None:
        super().__init__()

        self.model = root
        self.server = server

        self.setupUi(self)

        self.update_from_model()
        self.wire_signals()

    def wire_signals(self):
        def set_selection_down(node: Union[JenkinsFolder, JenkinsJob], selected: Selection):
            node.selected = selected

            if isinstance(node, JenkinsFolder):
                for folder in node.folders:
                    set_selection_down(folder, selected)

                for job in node.jobs:
                    job.selected = selected

        def set_selection_up(node: Union[JenkinsFolder, JenkinsJob]):
            parent = node.parent
            if not parent:
                return

            status: Optional[Selection] = None

            for child in itertools.chain(parent.folders, parent.jobs):
                if status is None:
                    status = child.selected
                    continue

                if child.selected != status:
                    parent.selected = Selection.PARTIAL
                    set_selection_up(parent)
                    return

            assert status
            parent.selected = status
            set_selection_up(parent)

        @action
        def item_changed(item: QTreeWidgetItem, index: int):
            node = item.data(1, 0)
            selected = as_selection(item.checkState(index))
            set_selection_down(node, selected)
            set_selection_up(node)

        self.tree_widget.itemChanged.connect(item_changed)

    @render
    def update_from_model(self):
        self.update_root_level()

    @render
    def update_root_level(self):
        child_node = create_node(self.model)
        self.tree_widget.addTopLevelItem(child_node)

        self.update_node_data(child_node, self.model)
        self.update_folder_level(child_node, self.model)

        self.tree_widget.expandAll()

    @render
    def update_folder_level(self,
                            parent_node,
                            folder: JenkinsFolder):
        for sub_folder in folder.folders:
            child_node = create_node(sub_folder)
            parent_node.addChild(child_node)

            self.update_node_data(child_node, sub_folder)
            self.update_folder_level(child_node, sub_folder)

        for job in folder.jobs:
            child_node = create_node(job)
            parent_node.addChild(child_node)

            self.update_node_data(child_node, job)

    @render(ignore_updates=True)
    def update_node_data(self,
                         child_node: QTreeWidgetItem,
                         item: Union[JenkinsJob, JenkinsFolder]):
        icon = "job.png" if isinstance(item, JenkinsJob) else "folder.png"
        child_node.setText(0, item.name)
        child_node.setIcon(0, get_icon(icon))
        child_node.setCheckState(0, as_qt_selection(item.selected))


def create_node(item: Any) -> QTreeWidgetItem:
    child_node = QTreeWidgetItem()
    child_node.setFlags(child_node.flags() | Qt.ItemIsUserCheckable)
    child_node.setCheckState(0, Qt.CheckState.Checked)
    child_node.setData(1, 0, item)

    return child_node

