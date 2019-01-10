###meteoPath GUI start screen
#  -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainapp.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.resize(484, 853)
        Dialog.setStyleSheet("background-color: rgb(101, 200, 205);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setPixmap(QtGui.QPixmap('img\Artboard 2.png'))
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "meteoPATH startscreen", None))

