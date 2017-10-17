# coding: utf-8
import os
from PyQt5 import uic
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtGui import QPixmap


def loadUi(path='./', name='test.ui'):
    # 加载ui文件并返回一个元组:(ui_window,qtbase)
    uifile = os.path.join(path, name)
    if os.path.exists(uifile):
        return uic.loadUiType(uifile)
    else:
        return (None, None)


def buildCacheDir(path='/tmp/netEase'):
    '创建缓存目录'
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def setLogo(obj, logoPath=None, scale=(100, 100)):
    '''设置图标
    logo -- 图片路径
    '''
    if logoPath:
        f = QFile(logoPath)
        f.open(QIODevice.ReadOnly)
        data = f.readAll()
        f.close()
        pic = QPixmap()
        pic.loadFromData(data)
        obj.setPixmap(pic.scaled(scale[0], scale[1]))
