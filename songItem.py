# coding: utf-8
'''歌曲类
记录一首歌需要的关键信息:ID，歌曲名，作者等
'''


class SongItem(object):
    name = ''  # 名称
    id = 0  # ID号
    artist = ''  # 作者
    time = ''  # 时长

    def __init__(self, name='', id=0, artist='', time='00:00'):
        self.name = name
        self.id = id
        self.artist = artist
        self.time = time
