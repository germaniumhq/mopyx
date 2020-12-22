# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ErrorFrame.ui',
# licensing of 'ui/ErrorFrame.ui' applies.
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
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.error_label = QtWidgets.QLabel(Form)
        self.error_label.setTextFormat(QtCore.Qt.RichText)
        self.error_label.setObjectName("error_label")
        self.horizontalLayout.addWidget(self.error_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.retry_button = QtWidgets.QPushButton(Form)
        self.retry_button.setObjectName("retry_button")
        self.horizontalLayout.addWidget(self.retry_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.error_name_label = QtWidgets.QLabel(Form)
        self.error_name_label.setWordWrap(True)
        self.error_name_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.error_name_label.setObjectName("error_name_label")
        self.verticalLayout.addWidget(self.error_name_label)
        self.error_stack_edit = QtWidgets.QPlainTextEdit(Form)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.error_stack_edit.setFont(font)
        self.error_stack_edit.setReadOnly(True)
        self.error_stack_edit.setPlainText("")
        self.error_stack_edit.setObjectName("error_stack_edit")
        self.verticalLayout.addWidget(self.error_stack_edit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.error_label.setText(QtWidgets.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Error</span></p></body></html>", None, -1))
        self.retry_button.setText(QtWidgets.QApplication.translate("Form", "Retry", None, -1))
        self.error_name_label.setText(QtWidgets.QApplication.translate("Form", "TextLabel", None, -1))

