# coding: utf-8

# 左边导航栏（侧边栏）模块，包含一下内容：
# - 推荐
# - 我的音乐
# - 收藏与创建歌单
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon
from uiloader import loadUi

ui_mainwindow, qtbaseclass = loadUi(name='navigation.ui')


class Navigation(ui_mainwindow, qtbaseclass):

    def __init__(self, parent=None):
        if parent==None:
            parent = self
        # super().__init__(parent)
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(self)
        self.initList()
        with open('QSS/navigation.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def initList(self):
        # 初始化列表信息

        # 设置推荐列表
        self.navigationList.addItem(QListWidgetItem(
            QIcon('resource/music.png'), " 发现音乐"))
        self.navigationList.addItem(QListWidgetItem(
            QIcon('resource/signal.png'), " 私人FM"))
        self.navigationList.addItem(QListWidgetItem(
            QIcon('resource/movie.png'), " MV"))
        self.navigationList.setCurrentRow(0)

        # 设置我的音乐
        self.nativeList.addItem(QListWidgetItem(
            QIcon('resource/notes.png'), " 本地音乐"))

        # 设置收藏与创建的歌单
        # 未实现（动态添加）