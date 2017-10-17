# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from uiloader import loadUi
from songsframe import SongsFrame
from albumdetailview import AlbumDetailView
from songItem import SongItem
# import api
from apis.netEaseApi import netease

ui_mainwindow, qtbaseclass = loadUi(name='mainwindow.ui')


class MainWindow(ui_mainwindow, qtbaseclass):

    # 详情页面
    detail = None
    # 当前播放列表
    playList = []
    # 当前播放的歌曲在列表中的索引号
    songIndex = 0
    # 当前播放的歌曲
    song = None
    # 播放器
    player = None
    # api
    func = netease
    # 是否循环播放
    loop = True

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
        ''' 初始化播放控件状态'''
        self.player = QMediaPlayer(self)
        self.player.setVolume(100)
        self.player.stateChanged.connect(self.slot_player_stateChanged)
        self.player.positionChanged.connect(self.slot_player_positionChanged)
        self.player.durationChanged.connect(self.slot_player_durationChanged)

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
        self.detail.addSongs.connect(self.slot_addSongs)

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

    def slot_play_clicked(self):
        '''播放 点击事件'''
        if self.player.mediaStatus() > 1 and self.player.mediaStatus() < 7:
            self.player.play()
            self.playButton.hide()
            self.pauseButton.show()
        else:
            # 未添加 音乐
            pass

    def slot_pause_clicked(self):
        '''暂停 点击事件'''
        self.player.pause()
        self.playButton.show()
        self.pauseButton.hide()

    def slot_addSongs(self, songsList):
        '''添加歌曲'''
        # 去重合并列表
        ids = [x.id for x in self.playList]
        for song in songsList:
            if song.id not in ids:
                self.playList.append(song)
        if self.song == None:
            self.song = self.playList[self.songIndex]
            try:
                mp3 = self.func.singsUrl([self.song.id])
                if mp3:
                    mp3 = mp3[0]['url']
                self.player.setMedia(QMediaContent(QtCore.QUrl(mp3)))
            except:
                # 网络异常
                pass

    def slot_player_stateChanged(self):
        '''播放器状态变化'''
        if not self.playList:
            return

        if self.player.state() == QMediaPlayer.StoppedState:
            if self.loop:
                self.songIndex = (self.songIndex + 1) % len(self.playList)
                self.song = self.playList[self.songIndex]
                try:
                    mp3 = self.func.singsUrl([self.song.id])
                    if mp3:
                        mp3 = mp3[0]['url']
                    self.player.setMedia(QMediaContent(QtCore.QUrl(mp3)))
                except:
                    # 网络异常
                    QMessageBox.warning(self, '获取音乐地址失败！请检查网络后重试！', '警告')
                self.player.play()
            else:
                self.playButton.show()
                self.pauseButton.hide()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.playButton.show()
            self.pauseButton.hide()
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.playButton.hide()
            self.pauseButton.show()

        self.countTime.setText(self.song.time)

    def slot_player_positionChanged(self, pos):
        '''播放时间改变控件位置'''
        t = self.player.position() / 1000
        mins = t // 60
        secs = t % 60
        curTime = QtCore.QTime(0, mins, secs).toString('mm:ss')
        self.currentTime.setText(curTime)
        # if self.song and float(self.song.time.replace(':', '.')) > 0:
        #     curSlider = float(curTime.replace(':', '.')
        #                       ) // float(self.song.time.replace(':', '.'))
        self.timeSlider.setValue(pos)

    def slot_player_durationChanged(self, duration):
        self.timeSlider.setRange(0, duration)
