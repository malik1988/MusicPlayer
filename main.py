#coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon

from navigation import Navigation
from maincontent import MainContent
from searcharea import SearchArea

class Window(QWidget):
    '''承载整个界面'''
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('音乐播放器')
        self.setWindowIcon(QIcon('resource/format.ico'))
        with open('QSS/window.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.resize(1022, 670)
        self.mainLayout=QHBoxLayout(self)
        na=Navigation()
        self.mainLayout.addWidget(na)
        main=MainContent()
        self.mainLayout.addWidget(main)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(QSS)
    l = Window()
    l.show()
    sys.exit(app.exec_())
