# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject

i18nStrings = None


class Strings(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strTitle = self.tr('Schedule')
        self.strExit = self.tr('Exit')
        self.strShowWindow = self.tr('Show Window')
        self.strHideWindow = self.tr('Hide Window')
        self.strAbout = self.tr('About')


def GetStrings():
    global i18nStrings
    if i18nStrings is None:
        i18nStrings = Strings()
    return i18nStrings
