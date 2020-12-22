# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/AddJobsFromServer.ui',
# licensing of 'ui/AddJobsFromServer.ui' applies.
#
# Created: Wed Nov 21 06:55:09 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 538)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.server_name_label = QtWidgets.QLabel(Dialog)
        self.server_name_label.setObjectName("server_name_label")
        self.verticalLayout.addWidget(self.server_name_label)
        self.content_holder = QtWidgets.QVBoxLayout()
        self.content_holder.setObjectName("content_holder")
        self.verticalLayout.addLayout(self.content_holder)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.select_button = QtWidgets.QPushButton(Dialog)
        self.select_button.setObjectName("select_button")
        self.horizontalLayout.addWidget(self.select_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Select jobs...", None, -1))
        self.server_name_label.setText(QtWidgets.QApplication.translate("Dialog", "Server Name", None, -1))
        self.close_button.setText(QtWidgets.QApplication.translate("Dialog", "Close", None, -1))
        self.select_button.setText(QtWidgets.QApplication.translate("Dialog", "Select", None, -1))

