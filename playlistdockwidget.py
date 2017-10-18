# coding: utf-8
# 播放列表界面
# Dock 停靠在main之中

from uiloader import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

uiBaseClass, qtBaseclass = loadUi(name='playlistdockwidget.ui')


class PlayListDockWidget(uiBaseClass, qtBaseclass):

    lastItem = None
    # 双击事件,int 为songIndex
    doubleClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        uiBaseClass.__init__(self)
        qtBaseclass.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.initTableWidget()

    def initTableWidget(self):
        header = ('音乐', '歌手',  '时长')
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)

        # 设置列宽。
        # self.tableWidget.setColumnWidth(0, 40)
        # self.tableWidget.setColumnWidth(1, 40)
        # self.tableWidget.setColumnWidth(2, 360)
        # self.tableWidget.setColumnWidth(3, 140)
        # self.tableWidget.setColumnWidth(4, 140)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置充满表宽。
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 设置表头亮度。
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        # 设置每次选择为一行。
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置垂直表头不显示。
        self.tableWidget.verticalHeader().setVisible(False)

    def setList(self, songsList):
        '''设置播放列表
        songsList - song类的列表[song]
        '''
        #
        listLen = len(songsList)
        self.setWindowTitle('播放列表： %d首歌曲' % listLen)
        self.tableWidget.setRowCount(listLen)
        for i, song in enumerate(songsList):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(song.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(song.artist))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(song.time))
        self.lastItem = None

    def setSelectRow(self, row):
        if self.lastItem:
            self.lastItem.setIcon(QIcon())
        self.tableWidget.setCurrentCell(row, 0)
        # self.tableWidget.item(row,0)
        item = self.tableWidget.currentItem()
        item.setIcon(QIcon('resource/playAll.png'))
        # 记录这次的作为下一次的上一次item
        self.lastItem = item

    def slot_tableCell_doubleClicked(self, row, column):
        '''表格内容双击事件'''
        self.doubleClicked.emit(row)
        self.setSelectRow(row)
