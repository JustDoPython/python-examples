# coding=utf-8
import os

from qqMusic import QQMusic
from miguMusic import MiGuMusic
from prettytable import PrettyTable


class MusicBox(object):

    def __init__(self):
        pass

    def download(self, data, songName, type):

        save_path = 'music/' + songName + '.' + type
        file = 'music'
        if os.path.exists(file):
            pass
        else:
            os.mkdir('music')

        try:
            print("{}下载中.....".format(songName), end='')
            with open(save_path, 'wb') as f:
                f.write(data)
            print("已下载完成")
        except Exception as err:
            print("文件写入出错:", err)
            return None

    def main(self):
        print('请输入需要下载的歌曲或者歌手：')
        key = input()
        print('正在查询..\033[32mQQ音乐\033[0m', end='')
        qqMusic = QQMusic()
        qq_song_list = qqMusic.main(key)
        print('...\033[31m咪咕音乐\033[0m')
        miguMusic = MiGuMusic()
        migu_song_list = miguMusic.main(key)

        qq_song_list.extend(migu_song_list)
        song_dict = {}
        for song in qq_song_list:
            key = song['name'] + '\\' + song['singer']
            s = song_dict.get(key)
            if s:
                if s['msg'] != 'Y':
                    song_dict[key] = song
            else:
                song_dict[key] = song

        i = 0

        table = PrettyTable(['序号', '歌手', '下载', '歌名'])
        table.border = 0
        table.align = 'l'
        for song in list(song_dict.values()):
            i = i + 1
            table.add_row([str(i), song['singer'], song['msg'], song['name']])
        print(table)

        while 1:
            print('\n请输入需要下载，按 q 退出：')
            index = input()
            if index == 'q':
                return

            song = list(song_dict.values())[int(index) - 1]
            data = qqMusic.get_request(song['downloadUrl'])
            if song['msg'] == 'Y':
                self.download(data.content, song['name'], song['type'])
            else:
                print('该歌曲不允许下载')

if __name__ == '__main__':
    musicBox = MusicBox()
    musicBox.main()