# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AddServerDialog.ui',
# licensing of 'ui/AddServerDialog.ui' applies.
#
# Created: Wed Nov 21 06:55:09 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 258)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.loading_content_holder = QtWidgets.QVBoxLayout()
        self.loading_content_holder.setObjectName("loading_content_holder")
        self.gridLayout.addLayout(self.loading_content_holder, 7, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 5, 0, 1, 1)
        self.url_edit = QtWidgets.QLineEdit(Dialog)
        self.url_edit.setObjectName("url_edit")
        self.gridLayout.addWidget(self.url_edit, 1, 1, 1, 1)
        self.name_edit = QtWidgets.QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.gridLayout.addWidget(self.name_edit, 0, 1, 1, 1)
        self.user_edit = QtWidgets.QLineEdit(Dialog)
        self.user_edit.setObjectName("user_edit")
        self.gridLayout.addWidget(self.user_edit, 4, 1, 1, 1)
        self.password_edit = QtWidgets.QLineEdit(Dialog)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setObjectName("password_edit")
        self.gridLayout.addWidget(self.password_edit, 5, 1, 1, 1)
        self.user_label = QtWidgets.QLabel(Dialog)
        self.user_label.setObjectName("user_label")
        self.gridLayout.addWidget(self.user_label, 4, 0, 1, 1)
        self.auth_check_box = QtWidgets.QCheckBox(Dialog)
        self.auth_check_box.setObjectName("auth_check_box")
        self.gridLayout.addWidget(self.auth_check_box, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.test_server_button = QtWidgets.QPushButton(Dialog)
        self.test_server_button.setObjectName("test_server_button")
        self.horizontalLayout.addWidget(self.test_server_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.add_button = QtWidgets.QPushButton(Dialog)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.name_edit, self.url_edit)
        Dialog.setTabOrder(self.url_edit, self.auth_check_box)
        Dialog.setTabOrder(self.auth_check_box, self.user_edit)
        Dialog.setTabOrder(self.user_edit, self.password_edit)
        Dialog.setTabOrder(self.password_edit, self.add_button)
        Dialog.setTabOrder(self.add_button, self.test_server_button)
        Dialog.setTabOrder(self.test_server_button, self.close_button)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Add Server...", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "URL <span style=\"color:red\">*</span>", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Name <span style=\"color:red\">*</span>", None, -1))
        self.password_label.setText(QtWidgets.QApplication.translate("Dialog", "Password", None, -1))
        self.user_label.setText(QtWidgets.QApplication.translate("Dialog", "User", None, -1))
        self.auth_check_box.setText(QtWidgets.QApplication.translate("Dialog", "Authentication", None, -1))
        self.test_server_button.setText(QtWidgets.QApplication.translate("Dialog", "Test", None, -1))
        self.close_button.setText(QtWidgets.QApplication.translate("Dialog", "Close", None, -1))
        self.add_button.setText(QtWidgets.QApplication.translate("Dialog", "Add", None, -1))

