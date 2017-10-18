# coding: utf-8
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QThread, Qt, pyqtSignal, QFile, QIODevice


class Downloader(QThread):
    """网络下载器
    savePath -- 为保存文件的路径
    """
    downloaded = pyqtSignal(str)

    def __init__(self, url, parent=None, savePath=0):
        super(Downloader, self).__init__(parent)
        self.url = QUrl(url)
        self.savePath = savePath

    def run(self):
        manager = QNetworkAccessManager()
        data = manager.get(QNetworkRequest(self.url))
        manager.finished.connect(self.save)
        self.exec_()

    def save(self, data):
        f = QFile(self.savePath)
        f.open(QIODevice.WriteOnly)
        data = data.readAll()
        f.write(data)
        f.flush()
        f.close()
        self.downloaded.emit(self.savePath)


class DownloaderManager(QThread):
    downloaders = []

    def __init__(self, parent=None, downloaderList=[]):
        super(DownloaderManager, self).__init__(parent)
        self.downloaders = downloaderList

    def run(self):
        # d=Downloader()
        # self.downloaders.append()
        for d in self.downloaders:
            d.start()
