# coding: utf-8
'''测试入口
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from mainwindow import MainWindow
from songsgroupbox import SongsGroupBox
from songsframe import SongsFrame
from albumdetailview import AlbumDetailView
from playlistdockwidget import PlayListDockWidget


from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore


class Mp3Player(QWidget):
    def __init__(self):
        # super(Mp3Player, self).__init__(self)
        QWidget.__init__(self)
        self.player = QMediaPlayer(self)
        mp3 = QtCore.QUrl.fromLocalFile(
            '/tmp/2b5c07d6d9d32958d77f76546c36f5a8.mp3')
        self.player.setMedia(QMediaContent(mp3))
        self.player.play()


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        widget = self.testWidget()
        bl = QVBoxLayout()
        self.setLayout(bl)
        bl.setSpacing(0)
        bl.setContentsMargins(0, 0, 0, 0)
        w = AlbumDetailView(self)
        bl.addWidget(w)
        bl.addWidget(widget)

    def testWidget(self):
        # w=Navigation(self)
        # w=MainContent(self)
        # w=NetEaseSearchResultFrame(self)
        # w = MainWindow(self)
        # w = SongsGroupBox(self)
        # w.setText(name='测试名称111111', author='作者：11后发生了无机化工拉萨')
        # w.setLogoByUrl(
        #     logoUrl='http://p1.music.126.net/n5LK7YKyuVqgNBXUfPJzww==/109951163042025818.jpg')
        # w = SongsFrame(self)
        # w.load()

        # w = AlbumDetailView(self)
        # w.setAlbum(id=916906701)
        # w = Mp3Player()
        w = PlayListDockWidget(self)
        return w


class DockMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        w = PlayListDockWidget(self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(QSS)
    # l = Window()
    l = MainWindow()
    # l = DockMainWindow()
    l.show()
    sys.exit(app.exec_())
