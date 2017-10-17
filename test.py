# coding: utf-8
'''测试入口
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from mainwindow import MainWindow
from songsgroupbox import SongsGroupBox
from songsframe import SongsFrame
from albumdetailview import AlbumDetailView


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        widget = self.testWidget()
        bl = QVBoxLayout()
        self.setLayout(bl)
        bl.setSpacing(0)
        bl.setContentsMargins(0, 0, 0, 0)
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

        w = AlbumDetailView(self)
        w.setAlbum(id=916906701)
        return w


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(QSS)
    # l = Window()
    l = MainWindow()
    l.show()
    sys.exit(app.exec_())
