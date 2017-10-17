#coding: utf-8

# 网易音乐模块
from uiloader import loadUi

ui_mainwindow, qtbaseclass = loadUi(name='neteasesingsframes.ui')

class NetEaseSearchResultFrame(ui_mainwindow, qtbaseclass):
    def __init__(self, parent=None):
        if parent==None:
            parent = self
        super().__init__(parent)
        self.setupUi(self)
        with open('QSS/searchArea.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.singsResultTable.setColumnCount(3)
        self.singsResultTable.setHorizontalHeaderLabels(('音乐标题','歌手','时长'))
        # 设置列宽度
        for i,width in zip(range(3), [self.width()/3*1.25,self.width()/3*1.25,self.width()/3*0.5]):
            self.singsResultTable.setColumnWidth(i,width)
        self.noSingsContentsLabel.hide()


