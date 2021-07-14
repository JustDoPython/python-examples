import requests
from requests.models import requote_uri
from bs4 import BeautifulSoup
import time
import random
import json
import re

url_file_name = 'D:\\url.txt'

def get_list():
    for p in range(500):
        html = requests.get('https://v.huya.com/g/all?set_id=31&order=hot&page={}'.format(p+1));
        soup = BeautifulSoup(html.text, 'html.parser')
        ul = soup.find('ul', class_='vhy-video-list w215 clearfix')
        lis = ul.find_all('li')
        for li in lis:
            a = li.find('a', class_ = 'video-wrap statpid');
            href = a.get('href')
            title = a.get('title')
            # 去掉文件名中的特殊字符
            title = validate_title(title)
            with open(url_file_name,'a',encoding = 'utf-8') as f:
                f.write(title + '|' + href + '\n')
        print("已经抓取了 {} 页".format(p + 1))
        time.sleep(random.randint(1, 9)/10)

def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title

def get_video_url():
    urls_file = open(url_file_name, 'r', encoding='utf-8')
    url_lines = urls_file.readlines()
    urls_file.close()
    
    video_urls = []
    for line in url_lines:
        # 视频名字 | 地址
        infos = line.split('|')
        video_id = infos[1].replace('.html\n', '').replace('/play/', '');
        data = requests.get('https://v-api-player-ssl.huya.com/?r=vhuyaplay%2Fvideo&vid={}&format=mp4%2Cm3u8'.format(video_id))
        data = json.loads(data.text)
        
        url = data['result']['items'][0]['transcode']['urls'][0]
        video_urls.append({'title': infos[0], 'url':url})

    return video_urls        
        
def save_video(video_urls):
    for item in video_urls:
        title = item.get('title')
        print('正在下载：{}'.format(title))
        html = requests.get(item.get('url'))
        data = html.content
        with open('D:\\{}.mp4'.format(title), 'wb') as f:
            f.write(data)
    print('全部下载完成了')

if __name__ == "__main__":
    get_list()
    video_urls = get_video_url()
    save_video(video_urls)
