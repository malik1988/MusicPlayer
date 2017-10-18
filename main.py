# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(QSS)
    l = MainWindow()
    l.show()
    sys.exit(app.exec_())
