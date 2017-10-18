# coding: utf-8
from PyQt5.QtGui import QPixmap
from uiloader import loadUi, buildCacheDir, setLogo
import os
from downloader import Downloader
from PyQt5.QtCore import pyqtSignal, Qt

uiBaseClass, qtBaseclass = loadUi(name='songsgroupbox.ui')

'''歌单界面
'''

cacheDir = buildCacheDir()


class SongsGroupBox(uiBaseClass, qtBaseclass):
    __slots__ = ('author', 'logo', 'name')
    clicked = pyqtSignal(int, str)
    downloader = None
    # 记录LOGO文件存储路径
    logoPath = None

    def __init__(self, parent=None, id=0):
        if parent == None:
            parent = self
        uiBaseClass.__init__(self)
        qtBaseclass.__init__(self)
        self.setupUi(self)
        self.setStyleSheet('QGroupBox{border: 0px;}')
        # 记录当前ID号
        self.id = id

    def setId(self, id=0):
        '''设置ID号'''
        self.id = id

    def setText(self, name='', author='', toolTip=''):
        ''' 设置歌单显示的名称，作者信息等'''

        self.name.setText(name)
        self.author.setText(author)
        self.setToolTip(toolTip)
        self.logo.setToolTip(toolTip)
        self.name.setToolTip(toolTip)
        self.author.setToolTip(author)

    def setLogoByUrl(self, logoUrl=''):
        ''' 通过url的方式设置logo'''
        path = '%s/%d.png' % (cacheDir, self.id)
        self.logoPath = path
        if os.path.exists(path):
            setLogo(self.logo, path, (120, 120))
        else:
            self.downloader = Downloader(logoUrl, self.logo, path)
            self.downloader.downloaded.connect(self.slot_pic_downloaded)
            self.downloader.start()

    def mousePressEvent(self, event):
        '''重写鼠标点击事件'''
        if event.buttons() == Qt.LeftButton:
            self.clicked.emit(self.id, self.logoPath)
            event.accept()
        else:
            event.ignore()

    def slot_pic_downloaded(self, savePath):
        '''图片下载完成'''
        setLogo(self.logo, savePath, (120, 120))
