#meteoPATH GUI start script
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import datetime
import copy
import mainappui, dataapp
from subprocess import Popen, PIPE
import time
from threading import Thread
import loc, process_app

class MainScreen(QtWidgets.QWidget, mainappui.Ui_Dialog):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        delay=100
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.secondWindow)
        self.timer.start(delay)
    def secondWindow(self):
        self.dialog=SecScreen()
        self.dialog.show()
class SecScreen(QtWidgets.QWidget, dataapp.Ui_Dialog):
    def __init__(self, parent=None):
        super(SecScreen, self).__init__(parent)
        self.setupUi(self)
        self.weather = QtCore.QProcess()
        self.twitter = QtCore.QProcess()
        self.weather.start('python "weather_app.py"')
        self.twitter.start('python "twitter_app.py"')
        locnow = loc.func()
        self.label_9.setText(str(locnow))
        list = process_app.get_data()
        self.textBrowser_2.setText(str(100 * list[0]) + ' %')
        self.textBrowser_6.setText(list[-1])
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", str(list[2]), None))
        self.label_7.setText(QtWidgets.QApplication.translate("Dialog", list[3], None))
        self.label_8.setText(QtWidgets.QApplication.translate("Dialog", str(list[1]), None))

        delay = 5000
        self.timer2 = QtCore.QTimer()
        self.timer2.setSingleShot(False)
        self.timer2.timeout.connect(self.texter)
        self.timer2.start(delay)
    def texter(self):
        list = process_app.get_data()
        self.textBrowser_2.setText(str(100 * list[0]) + ' %')
        self.textBrowser_6.setText(list[-1])
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", str(list[2]), None))
        self.label_7.setText(QtWidgets.QApplication.translate("Dialog", list[3], None))
        self.label_8.setText(QtWidgets.QApplication.translate("Dialog", str(list[1]), None))

app = QtWidgets.QApplication(sys.argv)
form = MainScreen()
form.setFocus()
form.show()
app.exec_()