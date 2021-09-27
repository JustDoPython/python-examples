# coding: utf8

import urllib.request
import requests as req
import time
import json


# 下载图片
def download_img(img_url, file_name):
    print(F'downloading {file_name}, img_url = {img_url}')
    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            with open(file_name, "wb") as f:
                f.write(response.read())  # 将内容写入图片
            return 'ok'
    except:
        return "fail"


def send_get(url, params):
    time.sleep(2)
    response = req.get(url, headers=None, params=params, verify=False)
    return response.text


def deal_result(result, page):
    index = page * 12
    for i in range(len(result)):
        img_url = result[i]['urls']['full']
        index += 1
        download_img(img_url, str(index) + '.png')


def loop():
    for i in range(3):
        url = 'https://unsplash.com/napi/photos?per_page=12&page=' + str(i)
        print(F'page = {i}, url = {url}')
        response = json.loads(send_get(url, None))
        deal_result(response, i)


if __name__ == '__main__':
    loop()
