# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dso-gui.ui'
#
# Created: Sun Jul  3 11:18:57 2011
#      by: pyside-uic 0.2.8 running on PySide 1.0.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1044, 650)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, -1, -1, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.delRowButton = QtGui.QPushButton(self.centralwidget)
        self.delRowButton.setObjectName("delRowButton")
        self.gridLayout.addWidget(self.delRowButton, 1, 0, 1, 1)
        self.AddRowBeforeButton = QtGui.QPushButton(self.centralwidget)
        self.AddRowBeforeButton.setObjectName("AddRowBeforeButton")
        self.gridLayout.addWidget(self.AddRowBeforeButton, 2, 0, 1, 1)
        self.AddButtonAfterButton = QtGui.QPushButton(self.centralwidget)
        self.AddButtonAfterButton.setObjectName("AddButtonAfterButton")
        self.gridLayout.addWidget(self.AddButtonAfterButton, 3, 0, 1, 1)
        self.SavenExitButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.SavenExitButton.sizePolicy().hasHeightForWidth())
        self.SavenExitButton.setSizePolicy(sizePolicy)
        self.SavenExitButton.setObjectName("SavenExitButton")
        self.gridLayout.addWidget(self.SavenExitButton, 4, 0, 1, 1)
        self.ClosewoSaveButton = QtGui.QPushButton(self.centralwidget)
        self.ClosewoSaveButton.setObjectName("ClosewoSaveButton")
        self.gridLayout.addWidget(self.ClosewoSaveButton, 5, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.delRowButton.setText(QtGui.QApplication.translate("MainWindow", "Удалить строку", None, QtGui.QApplication.UnicodeUTF8))
        self.AddRowBeforeButton.setText(QtGui.QApplication.translate("MainWindow", "Добавить строку до", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButtonAfterButton.setText(QtGui.QApplication.translate("MainWindow", "Добавить строку после", None, QtGui.QApplication.UnicodeUTF8))
        self.SavenExitButton.setText(QtGui.QApplication.translate("MainWindow", "СОХРАНИТЬ И ВЫЙТИ", None, QtGui.QApplication.UnicodeUTF8))
        self.ClosewoSaveButton.setText(QtGui.QApplication.translate("MainWindow", "ЗАКРЫТЬ БЕЗ СОХРАНЕНИЯ", None, QtGui.QApplication.UnicodeUTF8))

