# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/SelectJobsFrame.ui',
# licensing of 'ui/SelectJobsFrame.ui' applies.
#
# Created: Wed Nov 21 06:55:09 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tree_widget = QtWidgets.QTreeWidget(Form)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setObjectName("tree_widget")
        self.tree_widget.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.tree_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

