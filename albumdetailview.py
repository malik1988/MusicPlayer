# coding: utf-8
'''歌单详情'''

import api
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTime
from uiloader import loadUi, setLogo

uiBaseClass, qtBaseclass = loadUi(name='albumdetailview.ui')


class AlbumDetailView(uiBaseClass, qtBaseclass):

    def __init__(self, parent=None):
        uiBaseClass.__init__(self)
        qtBaseclass.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.func = api.WebApi()
        self.initTableWidget()

    def initTableWidget(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            [' ', '操作', '音乐', '歌手', '专辑', '时长'])
        # 设置列宽。
        self.tableWidget.setColumnWidth(0, 40)
        self.tableWidget.setColumnWidth(1, 40)
        self.tableWidget.setColumnWidth(2, 360)
        self.tableWidget.setColumnWidth(3, 140)
        self.tableWidget.setColumnWidth(4, 140)
        self.tableWidget.setColumnWidth(5, 60)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置充满表宽。
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 设置表头亮度。
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        # 设置每次选择为一行。
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置垂直表头不显示。
        self.tableWidget.verticalHeader().setVisible(False)

    def setAlbum(self, id=0, logoPath=None):
        '''通过id设置歌单信息'''
        # 设置歌单logo
        setLogo(self.logo, logoPath, (180, 180))
        # 获取歌单
        details = self.func.details_playlist(id)

        self.name.setText('歌单：' + details['name'])
        self.author.setText('作者：' + details['creator']['nickname'])
        self.tags.setText('标签：『' + str(details['tags'])[1:-1] + '』')
        try:
            self.notes.setText('简介：〖' + details['description'][:30] + '〗')
            self.notes.setToolTip('简介：〖' + details['description'] + '〗')
            self.notes.setWordWrap(True)
        except TypeError:
            self.notes.setText('简介：〖〗')
            self.notes.setToolTip('简介：〖〗')
        # 设置歌单列表
        self.tableWidget.setRowCount(details['trackCount'])

        for i, track in enumerate(details['tracks']):
            # 第一列为序号 0,1,2,3...
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(
                QIcon('resource/playlist.png'), ''))
            name = track['bMusic']['name']
            if not name:
                name = track['name']
            self.tableWidget.setItem(i, 2, QTableWidgetItem(name))
            artist = ''
            for index, art in enumerate(track['artists']):
                artist += art['name']
                if index != len(track['artists']) - 1:
                    artist += '&'

            self.tableWidget.setItem(i, 3, QTableWidgetItem(artist))
            self.tableWidget.setItem(
                i, 4, QTableWidgetItem(track['album']['name']))

            minuties = track['bMusic']['playTime'] // 60000
            seconds = track['bMusic']['playTime'] // 1000 % 60
            time = QTime(0, minuties, seconds)
            self.tableWidget.setItem(
                i, 5, QTableWidgetItem(time.toString('mm:ss')))
