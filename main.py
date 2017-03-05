# coding=utf-8
import sys
import os
import platform
import time
import ctypes
import json
import codecs
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTranslator, QFileInfo, QTimer
from MyConfig import *
from MainWindow import MainWindow

if platform.system() == 'Windows':
    myAppId = 'jalon.schedule'  # Arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

Config = None
AppIcon = None
EXE_Flag = False

class ScheduleNode:
    def __init__(self, hour, min, content):
        self.hour = hour
        self.min = min
        self.content = content


class MainCtrl(MainWindow):
    def __init__(self):
        global Config
        super().__init__(AppIcon, EXE_Flag, Config.staysOnTop)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onTick)
        self.lastSec = 0
        self.schdData = []

        self.loadScheddule(Config.schedule_file)

        self.viewInit(self.schdData)
        self.timer.start()

    def loadScheddule(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as data_file:   
                data = json.load(data_file)
        except FileNotFoundError as err:
            print("FileNotFoundError: {0}".format(err))
            return

        if data == None or not('Schedule' in data):
            print('josn file error!')
            return
        
        for d in data['Schedule']:
            print(d)
            tl = d['time'].split(':')
            if len(tl) == 2:
                self.schdData.append(ScheduleNode(int(tl[0]), int(tl[1]), d['content']))

    
    def viewInit(self, data):
        if data == None or len(data) == 0:
            print('Schedule empty')
            self.viewSchedule(None, None)
            return
        
        localtime = time.localtime(time.time())
        self.lastSec = localtime.tm_sec
        self.viewSchedule(None, data[0])

        dl = None
        for d in data:
            if d.hour > localtime.tm_hour or (d.hour == localtime.tm_hour and d.min > localtime.tm_min):
                break
            dl = d

        self.viewSchedule(dl, d)

    def onTick(self):
        data = self.schdData
        localtime = time.localtime(time.time())
        if localtime.tm_sec < self.lastSec:
            dl = None
            dn = None
            for d in data:
                if dl:
                    dn = d
                    break
                elif d.hour == localtime.tm_hour and d.min == localtime.tm_min:
                    dl = d

            if dl:
                if dn == None:
                    dn = data[0]
                self.viewSchedule(dl, dn)
                self.showWindow()
                print('{0:02d}:{1:02d}  {2}'.format(dl.hour, dl.min, dl.content))

        self.lastSec = localtime.tm_sec


    def close(self):
        self.timer.stop()
        super().close()
        print('exit')


def GetDataPath(package, resource):
    p = os.path.join(package, resource)
    if os.path.exists(p):
        print(p)
        return p

    try:
        d = os.path.dirname(sys.modules[package].__file__)
        p = os.path.join(d, resource)
        if os.path.exists(p):
            print(p)
            return p
    except AttributeError:
        pass
    
    return None


def main():
    global Config
    global EXE_Flag
    global AppIcon

    app = QApplication(sys.argv)

    filename = sys.argv[0]
    if filename.split('.')[1] == 'exe':
        iconF = QFileIconProvider()
        AppIcon = iconF.icon(QFileInfo(filename))
        EXE_Flag = True
    else:
        AppIcon = QIcon('Resource/clock.ico')

    Config = ConfigData()

    # Language
    print('Language: ' + Config.lang)
    file_path = GetDataPath('i18n', Config.lang + '.qm')
    trans = QTranslator()
    if not file_path or not trans.load(file_path) or not app.installTranslator(trans):
        print('Failed to load translator file!')

    m = MainCtrl()
    m.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
