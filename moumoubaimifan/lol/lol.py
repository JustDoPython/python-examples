from gevent import monkey; monkey.patch_all()
import requests
import gevent
import os
import re


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

root_path = 'D:\LOL'

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)   

def crawling():
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    resp = requests.get(url=url, headers=header)
    heros = resp.json()['hero']
    index = 0
    task_list = []
    for hero in heros:
        index = index + 1

        heroId = hero['heroId']
        hero_url = f'https://game.gtimg.cn/images/lol/act/img/js/hero/{heroId}.js'
        hero_resp = requests.get(url=hero_url, headers=header)
        skins = hero_resp.json()['skins']

        task = gevent.spawn(get_pic, skins)
        task_list.append(task)
        if len(task_list) == 10 or len(skins) == index:
            gevent.joinall(task_list)
            task_list = []
    


def get_pic(skins):
    for skin in skins:

        dir_name = skin['heroName'] + '_' + skin['heroTitle']
        pic_name = ''.join(skin['name'].split(skin['heroTitle'])).strip();
        url = skin['mainImg']
        
        if not url:
            continue 

        invalid_chars='[\\\/:*?"<>|]'
        pic_name = re.sub(invalid_chars,'', pic_name)
        download(dir_name, pic_name, url)

def download(dir_name, pic_name, url):
    print(f'{pic_name} 下载完成, {url}')
    dir_path = f'{root_path}\{dir_name}'
    mkdir(dir_path)
    
    resp = requests.get(url, headers=header)
    with open(f'{dir_path}\{pic_name}.png', 'wb') as f:
        f.write(resp.content)
    print(f'{pic_name} 下载完成')

if __name__ == '__main__':
    mkdir(root_path)
    crawling()
