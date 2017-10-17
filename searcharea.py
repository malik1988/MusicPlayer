# coding: utf-8
# 搜索界面
# - 显示当前搜索条件
# - 显示搜索结果

from uiloader import loadUi

ui_mainwindow, qtbaseclass = loadUi(name='searcharea.ui')


class SearchArea(ui_mainwindow, qtbaseclass):
    def __init__(self, parent=None):
        if parent==None:
            parent = self
        super().__init__(parent)
        self.setupUi(self)
        with open('QSS/searchArea.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def setText(self, text):
        # 设置搜索条件显示字符
        self.titleLabel.setText(
            "搜索<font color='#23518F'>“{0}”</font><br>".format(text))
    def setSingsFrame(self):
        # 设置结果
        # self.contentsTab.addTab()
        pass
