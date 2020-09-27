# coding=utf-8
import json

import requests
from urllib.parse import quote
import urllib


class MiGuMusic(object):

    def __init__(self):
        pass

    def get_request(self, url, params = None):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response
            else:
                return None
        except TimeoutError:
            print("网络不佳，请重新下载")
            return None
        except Exception as err:
            print("请求出错：", err)
            return None



    def search_music(self, key):
        pagesize = "10"

        url = 'http://m.music.migu.cn/migu/remoting/scr_search_tag'
        key = urllib.parse.quote(key)
        params = {'rows': pagesize, 'type': 2, 'keyword': key, 'pgc': 1, }
        resp = self.get_request(url, params=params)

        resp.encoding = 'utf-8'
        resp_json = json.loads(resp.text)

        musics = resp_json["musics"]
        song_list = []

        for song in musics:
            resp = self.get_request(song['mp3'])
            if resp:
                msg = 'Y'
            else:
                msg = 'N'

            song_list.append({'name': song['songName'], 'songmid': None, 'singer': song['singerName'],
                              'downloadUrl': song['mp3'], 'msg': msg, 'type': 'mp3'})
        return song_list

    def main(self, key):
        song_list = self.search_music(key)
        return song_list

if __name__ == '__main__':
    miguMusic = MiGuMusic()
    miguMusic.search_music('陈奕迅')