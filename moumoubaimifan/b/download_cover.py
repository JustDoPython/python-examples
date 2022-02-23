import requests
import pathlib
import shutil
import json

base_url = 'https://api.bilibili.com/x/space/arc/search?mid=320491072&ps=30&tid=0&pn={0}&keyword=&order=pubdate&jsonp=jsonp'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

def get_total_page():
    response = requests.get(base_url.format(1), headers=headers)
    j = response.content
    data = json.loads(j)
    page = data['data']['page']
    return int(page['count'] / page['ps']) + 1
 

def get_image_urls():
    total_page = get_total_page()+1

    for i in range(1, total_page):
        url = base_url.format(i)
        response = requests.get(url, headers=headers)
        j = response.content
        data = json.loads(j)
        for i in data['data']['list']['vlist']:
            yield {'name': i['title'], 'url': i["pic"]}


def remove_unvalid_chars(s):
    for c in r'''"'<>/\|:*?''':
        s = s.replace(c, '')
    return s


def download_images():
    save_folder = r'~/Desktop/images'
    folder = pathlib.Path(save_folder).expanduser()
    if not folder.exists():
        folder.mkdir()
    for i in get_image_urls():
        response = requests.get(i['url'], stream=True)
        filename = remove_unvalid_chars(i["name"])+'.jpg'
        with open(folder/filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f'{i["name"]}.jpg下载完成')


download_images()
