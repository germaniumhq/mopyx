# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/SingleBuildStatusFrame.ui',
# licensing of 'ui/SingleBuildStatusFrame.ui' applies.
#
# Created: Wed Nov 21 06:55:10 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(114, 42)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(2, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtWidgets.QToolButton(Form)
        self.icon.setCursor(QtCore.Qt.PointingHandCursor)
        self.icon.setStyleSheet("padding: 0;\n"
"border: none;")
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.icon.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))

