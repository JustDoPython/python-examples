# coding=utf-8
import random

import requests
import json


class QQMusic(object):


    def __init__(self):
        pass

    def get_request(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }
            response = requests.get(url, headers = headers)
            if response.status_code == 200:
                return response
        except Exception as e:
            print("请求出错：", e)

        return None


    def search_music(self, key):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=%d&w=%s' % (20, key)
        resp = self.get_request(url)
        resp_json = json.loads(resp.text[9:][:-1])
        data_song_list = resp_json['data']['song']['list']
        song_list = []
        for song in data_song_list:
            singers = [s.get("name", "") for s in song.get("singer", "")]
            song_list.append({'name': song['songname'], 'songmid': song['songmid'], 'singer': '|'.join(singers)})
        print(song_list)
        return song_list

    def download_url(self, song):
        guid = str(random.randrange(1000000000, 10000000000))

        purl_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?' \
                   '&data={"req":{"param":{"guid":" %s"}},' \
                          '"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}' \
                   % (guid, guid, song['songmid'], 0, 0)

        resp = self.get_request(purl_url)

        if resp is None:
            return 'N', 'None', '.m4a'

        resp_json = json.loads(resp.text)

        purl = resp_json['req_0']['data']['midurlinfo'][0]['purl']

        if len(purl) < 1:
            msg = 'N'

        download_url = 'http://ws.stream.qqmusic.qq.com/' + purl
        song_data = self.get_request(download_url)
        if song_data:
            msg = 'Y'

        return msg, download_url, '.m4a'


    def main(self, key):
        song_list = self.search_music(key)
        for song in song_list:
            msg, download_url, type = self.download_url(song)
            song['msg'] = msg
            song['downloadUrl'] = download_url
            song['type'] = type
        return song_list





