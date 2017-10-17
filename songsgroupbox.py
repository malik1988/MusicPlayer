# coding: utf-8
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QThread, Qt, pyqtSignal, QFile, QIODevice
from uiloader import loadUi, buildCacheDir, setLogo
import os

uiBaseClass, qtBaseclass = loadUi(name='songsgroupbox.ui')

'''歌单界面
'''

cacheDir = buildCacheDir()


class SongsGroupBox(uiBaseClass, qtBaseclass):
    __slots__ = ('author', 'logo', 'name')
    clicked = pyqtSignal(int, str)
    thread = None
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
            self.thread = Download(logoUrl, self.logo, path)
            self.thread.start()

    def mousePressEvent(self, event):
        '''重写鼠标点击事件'''
        if event.buttons() == Qt.LeftButton:
            self.clicked.emit(self.id, self.logoPath)
            event.accept()
        else:
            event.ignore()


class Download(QThread):
    """用于主页歌单等的图片加载。"""

    def __init__(self, url, parent=None, savePath=0):
        super(Download, self).__init__(parent)
        self.main = parent
        self.url = QUrl(url)
        self.manager = QNetworkAccessManager()
        self.savePath = savePath

    def run(self):
        data = self.manager.get(QNetworkRequest(self.url))
        self.manager.finished.connect(lambda: self.save_pic(data))
        self.exec_()

    def save_pic(self, data):
        f = QFile(self.savePath)
        f.open(QIODevice.WriteOnly)
        data = data.readAll()
        f.write(data)
        f.flush()
        f.close()
        pic = QPixmap()
        pic.loadFromData(data)
        self.main.setPixmap(pic.scaled(120, 120))
