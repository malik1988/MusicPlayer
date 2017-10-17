# coding: utf-8
'''歌单列表控件
'''
import api
from songsgroupbox import SongsGroupBox
from uiloader import loadUi

uiBaseClass, qtBaseclass = loadUi(name='songsframe.ui')


class SongsFrame(uiBaseClass, qtBaseclass):
    __slots__ = ('gridLayout', 'nexButton', 'prevButton')
    offset = 0
    step = 30  # 一次获取的步长 30个
    MAX = 10
    parent = None

    def __init__(self, parent=None):
        uiBaseClass.__init__(self)
        qtBaseclass.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.func = api.WebApi()
        self.load()

    def load(self, offset=0):
        '''加载界面'''
        try:
            details = self.func.all_playlist(offset=0)
            # print("load:\n", details)
        except:
            pass

        for index, item in zip(range(len(details)), details):
            logoUrl = item['coverImgUrl']
            name = item['name']
            author = 'by:' + item['creator']['nickname']
            songs = SongsGroupBox(parent=self, id=item['id'])
            songs.setText(name=name[:8], author=author[:8], toolTip=name)
            songs.setLogoByUrl(logoUrl=logoUrl)
            songs.clicked.connect(self.slot_clicked_id)
            self.gridLayout.addWidget(songs, (index + 0 - 0) / 5, index % 5)

    def reload(self, offset=0):
        try:
            details = self.func.all_playlist(offset=offset)
        except:
            pass

        for index, item in zip(range(len(details)), details):
            logoUrl = item['coverImgUrl']
            name = item['name']
            author = 'by:' + item['creator']['nickname']
            songs = self.gridLayout.itemAtPosition(
                index / 5, index % 5).widget()

            songs.setId(item['id'])

            # songs = SongsGroupBox(parent=self, id=item['id'])
            songs.setText(name=name[:8], author=author[:8], toolTip=name)
            songs.setLogoByUrl(logoUrl=logoUrl)
            songs.clicked.connect(self.slot_clicked_id)
            # self.gridLayout.addWidget(songs, (index + 0 - 0) / 5, index % 5)

    def slot_clicked_id(self, id, logoPath):
        # 歌单点击处理
        self.parent.tabWidget.hide()
        self.parent.detailView.show()
        self.parent.detail.setAlbum(id=id, logoPath=logoPath)

    def slot_prev_clicked(self):
        '''上一页点击事件'''
        if self.offset > 0:
            self.offset = self.offset - 1
            self.reload(self.offset * self.step)

    def slot_next_clicked(self):
        '''下一页点击事件'''
        if self.offset < self.MAX:
            self.offset = self.offset + 1
            self.reload(self.offset * self.step)
