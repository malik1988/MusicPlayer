# coding: utf-8
'''歌单详情'''

# import api
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTime, pyqtSignal
from uiloader import loadUi, setLogo
from songItem import SongItem
from apis.netEaseApi import netease
from downloader import DownloaderManager, Downloader

uiBaseClass, qtBaseclass = loadUi(name='albumdetailview.ui')


class AlbumDetailView(uiBaseClass, qtBaseclass):
    # 当前歌单中所有歌曲列表，只记录ID号
    trackList = []
    # 需要播放的歌曲列表
    # playList = []

    downloader = None

    addSongs = pyqtSignal(list)

    def __init__(self, parent=None):
        uiBaseClass.__init__(self)
        qtBaseclass.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.func = netease
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
        except:
            self.notes.setText('简介：〖〗')
            self.notes.setToolTip('简介：〖〗')
        # 设置歌单列表
        self.tableWidget.setRowCount(details['trackCount'])
        # 清空之前的列表信息
        self.trackList.clear()
        for i, track in enumerate(details['tracks']):
            # 歌曲ID号
            id = track['id']
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
            time = QTime(0, minuties, seconds).toString('mm:ss')
            self.tableWidget.setItem(
                i, 5, QTableWidgetItem(time))
            song = SongItem(name=name, id=id, artist=artist, time=time)

            self.trackList.append(song)

    def slot_playAll_clicked(self):
        '''播放全部 点击事件'''
        self.addSongs.emit(self.trackList)
        pass

    def slot_downloadAll_clicked(self):
        '''下载全部 点击事件'''
        # downList = []
        for song in self.trackList:
            url = self.func.singsUrl([song.id])
            if url:
                url = url[0]['url']
            path = '/tmp/netEase/mp3/%s.mp3' % song.name
            down = Downloader(url, parent=self, savePath=path)
            down.start()
            # downList.append(down)
        # self.downloader = DownloaderManager(self, downList)
        # self.downloader.start()

    def slot_tableCell_doubleClicked(self, row, column):
        '''歌曲列表 双击事件
        row - 表格中对应的行号，
        column - 表格中对应的列号
        '''
        songId = self.trackList[row]
        # self.playList.append(songId)
        self.addSongs.emit([songId])
