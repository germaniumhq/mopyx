# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/LoadingJobFrame.ui',
# licensing of 'ui/LoadingJobFrame.ui' applies.
#
# Created: Wed Nov 21 06:55:10 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(331, 163)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.job_name_label = QtWidgets.QLabel(Form)
        self.job_name_label.setObjectName("job_name_label")
        self.verticalLayout.addWidget(self.job_name_label)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.content = QtWidgets.QVBoxLayout()
        self.content.setObjectName("content")
        self.verticalLayout.addLayout(self.content)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.job_name_label.setText(QtWidgets.QApplication.translate("Form", "TextLabel", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Scanning branches...", None, -1))

