# 学习制作网易云音乐客户端。
# 此文件实现登陆查询等一系列功能。
__author__ = 'weiy'
"""
4.10日。
"""
import urllib.parse
import requests
import hashlib
import json


def shotlist(lst):
    """列表去重。"""
    temp1 = sorted(list(set(lst)))
    return temp1


class WebApi:
    """一些功能。"""
    default_timeout = 10
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Proxy-Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    }

    def __init__(self):
        self.cookies = {
            'appver': '1.6.1.82809',
            'os': 'pc'
        }

    def httpRequest(self, action, method="GET", add=None, data=None, headers=headers, cookies='',\
                    timeout=default_timeout, urlencode='utf-8'):
        """
            默认以get方式请求，
            GET方式附加内容用add参数，POST方式提交内容用data参数。
            编码用urlencode参数，默认utf-8。
            GET方式返回json形式请求的内容。
            POST方式返回cookies和json形式的内容。(0,1)
            默认cookies为空。
        """
        if method.upper() == 'GET':
            if add:
                html = requests.get(action, params=add, headers=headers, cookies=cookies, timeout=timeout)
            else:
                html = requests.get(action, headers=headers, cookies=cookies, timeout=timeout)
            html.encoding = urlencode
            return json.loads(html.text)
        elif method.upper() == 'POST':
            if data:
                html = requests.post(action, data=data, headers=headers, cookies=cookies, timeout=timeout)
            else:
                html = requests.post(action, headers=headers, cookies=cookies, timeout=timeout)
            html.encoding = urlencode
            return html.cookies, json.loads(html.text)

    def login(self, username, password):
        """
            以网易账号登陆，其他的登陆待写。返回cookies和json形式内容。
        """
        data = {
            'username': username,
            'password': hashlib.md5(password.encode('utf-8')).hexdigest(),
            'remeberLogin': 'true'
        }
        cki = self.httpRequest('http://music.163.com/api/login', method="POST", data=data)
        cki[0].set('appver', self.cookies['appver'], domain='music.163.com')
        cki[0].set('os', self.cookies['os'], domain='music.163.com')  
        return cki[0], cki[1]

    def user_playlist(self, uid, offset=0):
        """
            个人歌单。
        """
        url = 'http://music.163.com/api/user/playlist/?offset=%s&limit=1000&uid=%s' % (offset, uid)
        html = self.httpRequest(url, method='GET', cookies=self.cookies)
        return html['playlist']

    def all_playlist(self, cat='全部歌单', types='all', offset=0, index=1):
        """
            全部歌单。列表字典形式。
        """
        url = 'http://music.163.com/api/playlist/list?cat=%s&type=%s&order=%s&offset=%d&total=true&limit=30&index=%d)'\
            % (urllib.parse.quote(cat), types, types, offset, index)
        html = self.httpRequest(url, method='GET', cookies=self.cookies)
        return html['playlists']

    def details_playlist(self, id):
        """
            歌单详情。
        """
        url = 'http://music.163.com/api/playlist/detail?id=%d' % (id)
        html = self.httpRequest(url, method="GET", cookies=self.cookies)
        return html['result']

    def search(self, s, offset=0, limit=100, total='true', stype=1):
        """
            搜索.
            type类型: 单曲(1), 专辑(10), 歌手(100), 歌单(1000), 用户(1002)
        """
        url = 'http://music.163.com/api/search/get/web'
        data = {
            's': s,
            'offset': offset,
            'total': total,
            'limit': limit,
            'type': stype
        }
        html = self.httpRequest(url, method='POST', data=data, cookies=self.cookies)
        try:
            return html[1]['result']
        except:
            return "Not Found!"

    def details_search(self, id):
        """
            搜索结果详情，返回歌曲URL。
        """
        id = str(id)
        url = "http://music.163.com//api/song/detail/?id=%s&ids=%s" % (id, urllib.parse.quote('[%s]' % (id)))
        html = self.httpRequest(url, method='GET', cookies=self.cookies)
        return html['songs'][0]['mp3Url']

    def newsong(self, areaID=0, offset=0, total='true', limit=100):
        """
            最新音乐--新歌速递。
            areaID(0全部, 9华语, 96欧美, 16韩国, 8日本。)
        """
        url = 'http://music.163.com/api/discovery/new/songs?areaId=%d&offset=%d&total=%s&limit=%d' %\
              (areaID, offset, total, limit)
        html = self.httpRequest(url, method='GET', cookies=self.cookies)
        return html['data']

    def fnewsong(self, year=2015, month=4, area='ALL'):
        """
            最新音乐--新碟上架。
            area(ALL全部, ZH华语, EA欧美, KR韩国, 日本JP)
        """
        url = 'http://music.163.com/api/discovery/new/albums/area?year=%d&month=%d&area=%s&type=hot&offset=0&total=true&limit=20&rcmd=true' \
              % (year, month, area)
        html = self.httpRequest(url, method="GET", cookies=self.cookies)
        return html['monthData']

if __name__ == '__main__':
    main = WebApi()
    req = main.newsong()
    for i in req:
        print(i)
