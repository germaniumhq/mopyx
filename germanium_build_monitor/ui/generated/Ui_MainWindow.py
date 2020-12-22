# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui',
# licensing of 'ui/MainWindow.ui' applies.
#
# Created: Wed Nov 21 06:55:09 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(459, 524)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.current_view = QtWidgets.QVBoxLayout()
        self.current_view.setObjectName("current_view")
        self.verticalLayout.addLayout(self.current_view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 459, 23))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.about_felix_action = QtWidgets.QAction(MainWindow)
        self.about_felix_action.setObjectName("about_felix_action")
        self.about_qt_action = QtWidgets.QAction(MainWindow)
        self.about_qt_action.setObjectName("about_qt_action")
        self.minimize_action = QtWidgets.QAction(MainWindow)
        self.minimize_action.setObjectName("minimize_action")
        self.exit_action = QtWidgets.QAction(MainWindow)
        self.exit_action.setObjectName("exit_action")
        self.menu_File.addAction(self.minimize_action)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.exit_action)
        self.menu_Help.addAction(self.about_felix_action)
        self.menu_Help.addAction(self.about_qt_action)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Felix Build Monitor", None, -1))
        self.menu_File.setTitle(QtWidgets.QApplication.translate("MainWindow", "&File", None, -1))
        self.menu_Help.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Help", None, -1))
        self.about_felix_action.setText(QtWidgets.QApplication.translate("MainWindow", "&About Felix Build Monitor", None, -1))
        self.about_qt_action.setText(QtWidgets.QApplication.translate("MainWindow", "About &Qt", None, -1))
        self.minimize_action.setText(QtWidgets.QApplication.translate("MainWindow", "&Minimize", None, -1))
        self.exit_action.setText(QtWidgets.QApplication.translate("MainWindow", "E&xit", None, -1))

