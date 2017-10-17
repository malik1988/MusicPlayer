# coding: utf-8

# 主内容区

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon

from uiloader import loadUi

ui_mainwindow, qtbaseclass = loadUi(name='maincontent.ui')


class MainContent(ui_mainwindow, qtbaseclass):
    def __init__(self, parent=None):
        if parent==None:
            parent = self
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(self)
        with open('QSS/mainContent.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def addTab(self, widget, name=""):
        self.tab.addTab(widget, name)
