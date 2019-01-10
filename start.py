###Start data collection GUI

from PySide.QtCore import *
from PySide.QtGui import *

from PySide import QtCore, QtGui
import sys, os

import ui
from subprocess import Popen, PIPE
import datetime

class MainScreen(QWidget, ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.collect)
        self.pushButton_2.clicked.connect(self.store)
        self.pushButton_3.clicked.connect(self.collect_stop)
    def collect(self):
        self.weather = QtCore.QProcess()
        self.twitter = QtCore.QProcess()
        self.weather.readyReadStandardOutput.connect(self.read_out)
        self.twitter.readyReadStandardOutput.connect(self.read_out_2)
        self.weather.start('python "weather_collect.py"')
        self.twitter.start('python "stream_starter.py"')
        #self.pt = Popen([sys.executable, 'twitter_stream.py'], cwd=r"C:\Users\Karolina\OneDrive - Imperial College London\Year 4\Sensing\Coursework\code")
        #self.pw = Popen([sys.executable, 'weather_collect.py'], cwd=r"C:\Users\Karolina\OneDrive - Imperial College London\Year 4\Sensing\Coursework\code")
        #for line in self.pt.stdout.readlines():
        #    print line
        self.pushButton.hide()
        self.pushButton_3.show()
        time=str(datetime.datetime.now())
        self.textBrowser.setText('STARTED ' + time)
        self.textBrowser_2.setText('STARTED ' + time)
    def collect_stop(self):
        self.twitter.kill()
        self.weather.kill()
        #stop = Popen("stop.bat",cwd=r"C:\Users\Karolina\OneDrive - Imperial College London\Year 4\Sensing\Coursework\code")
        #self.pt.kill()
        #self.pw.kill()
        self.pushButton_3.hide()
        self.pushButton.show()
        time = str(datetime.datetime.now())
        self.textBrowser.append('STOPPED '+time)
        self.textBrowser_2.append('STOPPED '+time)
    def store(self):
        s = Popen("store.bat",cwd=os.getcwd(),stdout=PIPE,)
        time=str(datetime.datetime.now())
        self.textBrowser_3.setText(time)

    def read_out(self):
        self.textBrowser.append(str(self.weather.readAllStandardOutput()).strip())

    def read_out_2(self):
        self.textBrowser_2.append(str(self.twitter.readAllStandardOutput()).strip())

app = QApplication(sys.argv)
form = MainScreen()
form.setFocus()
form.show()
app.exec_()