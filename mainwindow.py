# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
from uiloader import loadUi
from songsframe import SongsFrame
from albumdetailview import AlbumDetailView

ui_mainwindow, qtbaseclass = loadUi(name='mainwindow.ui')


class MainWindow(ui_mainwindow, qtbaseclass):
    detail = None

    def __init__(self, parent=None):
        if parent == None:
            parent = self
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Music")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('resource/format.ico'))
        with open('QSS/mainWindow.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        # 初始化
        self.initList()
        self.initPlayWidgets()
        self.initTabWidgets()
        self.initDetailView()

    def initList(self):
        # 初始化列表信息

        # 设置推荐列表
        self.recommandList.addItem(QListWidgetItem(
            QIcon('resource/music.png'), " 发现音乐"))
        self.recommandList.addItem(QListWidgetItem(
            QIcon('resource/signal.png'), " 私人FM"))
        self.recommandList.addItem(QListWidgetItem(
            QIcon('resource/movie.png'), " MV"))
        self.recommandList.setCurrentRow(0)

        # 设置我的音乐
        self.myList.addItem(QListWidgetItem(
            QIcon('resource/notes.png'), " 本地音乐"))

        # 设置收藏与创建的歌单
        # 未实现（动态添加）

    def initPlayWidgets(self):
        # 初始化播放控件状态

        # 隐藏暂停按键
        self.pauseButton.hide()
        self.noVolume.hide()

    def initTabWidgets(self):
        # 初始化主窗口中TabWdidget
        self.detailView.hide()
        self.tabWidget.clear()
        netEase = SongsFrame(self)
        self.tabWidget.addTab(netEase, '网易云音乐')

    def initDetailView(self):
        # 初始化详情页
        self.detail = AlbumDetailView(self)
        self.detailView.setWidget(self.detail)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MiddleButton:
            # if event.globalPos().x() > self.pos().x():
            #     print("Y")
            # else:
            #     print('N')
            self.move(event.globalPos())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def slot_prev_page_clicked(self):
        '''上一页'''
        if self.tabWidget.isHidden():
            self.tabWidget.show()
            self.detailView.hide()

    def slot_next_page_clicked(self):
        '''下一页'''
        # if self.detailView.isHidden():
        #     self.tabWidget.hide()
        #     self.detailView.show()
        pass

    def slot_prev_song_clicked(self):
        '''上一首歌'''
        pass

    def slot_next_song_clicked(self):
        '''下一首歌'''
        pass
