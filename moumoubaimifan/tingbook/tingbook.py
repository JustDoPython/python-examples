from bs4 import BeautifulSoup
import requests
import re
import random
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

def get_detail_urls(url):
    url_list = []
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.select('.red12')[0].strong.text
    if not os.path.exists(name):
        os.makedirs(name)
    div_list = soup.select('div.list a')
    for item in div_list:
        url_list.append({'name': item.string, 'url': 'https://www.tingchina.com/yousheng/{}'.format(item['href'])})
    return name, url_list
    
def get_mp3_path(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, 'lxml')
    script_text = soup.select('script')[-1].string
    fileUrl_search = re.search('fileUrl= "(.*?)";', script_text, re.S)
    if fileUrl_search:
        return 'https://t3344.tingchina.com' + fileUrl_search.group(1)
        
def get_key(url):
    url = 'https://img.tingchina.com/play/h5_jsonp.asp?{}'.format(str(random.random()))
    headers['referer'] = url
    response = requests.get(url, headers=headers)
    matched = re.search('(key=.*?)";', response.text, re.S)
    if matched:
        temp = matched.group(1)
        return temp[len(temp)-42:]

if __name__ == "__main__":
    url = input("请输入浏览器书页的地址：")
    dir,url_list = get_detail_urls()

    for item in url_list:
        audio_url = get_mp3_path(item['url'])
        key = get_key(item['url'])
        audio_url = audio_url + '?key=' + key
        headers['referer'] = item['url']
        r = requests.get(audio_url, headers=headers,stream=True)
        with open(os.path.join(dir, item['name']),'ab') as f:
            f.write(r.content)
            f.flush()
