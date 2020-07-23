# !/usr/bin/python
# -*- coding:utf-8 -*-
import requests, time, urllib.request, re, json, sys
from bs4 import BeautifulSoup

class bilibili_crawl:

    def __init__(self, bv):
        # 视频页地址
        self.url = 'https://www.bilibili.com/video/' + bv
        # 下载开始时间
        self.start_time = time.time()

    def get_vedio_info(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            }

            response = requests.get(url = self.url, headers = headers)
            if response.status_code == 200:

                bs = BeautifulSoup(response.text, 'html.parser')
                # 取视频标题
                video_title = bs.find('span', class_='tit').get_text()

                # 取视频链接
                pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
                script = bs.find("script", text=pattern)
                result = pattern.search(script.next).group(1)

                temp = json.loads(result)
                # 取第一个视频链接
                for item in temp['data']['dash']['video']:
                    if 'baseUrl' in item.keys():
                        video_url = item['baseUrl']
                        break

                return {
                    'title': video_title,
                    'url': video_url
                }
        except requests.RequestException:
            print('视频链接错误，请重新更换')

    def download_video(self, video):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        url = video['url']
        filename = title + '.mp4'
        opener = urllib.request.build_opener()
        opener.addheaders = [('Origin', 'https://www.bilibili.com'),
                              ('Referer', self.url),
                              ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url = url, filename = filename, reporthook = self.schedule)

    def schedule(self, blocknum, blocksize, totalsize):
        '''
        urllib.urlretrieve 的回调函数
        :param blocknum: 已经下载的数据块
        :param blocksize: 数据块的大小
        :param totalsize: 远程文件的大小
        :return:
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        s = ('#' * round(percent)).ljust(100, '-')
        sys.stdout.write("%.2f%%" % percent + '[ ' + s +']' + '\r')
        sys.stdout.flush()

if __name__ == '__main__':
        bc = bilibili_crawl('BV1Vh411Z7j5')
        vedio = bc.get_vedio_info()
        bc.download_video(vedio)