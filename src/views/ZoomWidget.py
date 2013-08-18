# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\widget.ui'
#
# Created: Sun Aug 18 14:42:15 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ZoomBar(object):
    def setupUi(self, ZoomBar):
        self.setObjectName("ZoomBar")
        self.resize(221, 31)
        self.ZoomOut = QtGui.QPushButton(self)
        self.ZoomOut.setGeometry(QtCore.QRect(0, 0, 111, 31))
        self.ZoomOut.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.ZoomOut.setObjectName("ZoomOut")
        self.ZoomIn = QtGui.QPushButton(self)
        self.ZoomIn.setGeometry(QtCore.QRect(110, 0, 111, 31))
        self.ZoomIn.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.ZoomIn.setObjectName("ZoomIn")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("ZoomBar", "Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.ZoomOut.setText(QtGui.QApplication.translate("ZoomBar", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.ZoomIn.setText(QtGui.QApplication.translate("ZoomBar", "+", None, QtGui.QApplication.UnicodeUTF8))

