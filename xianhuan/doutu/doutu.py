#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import threading
import requests
from lxml import etree
import os
import random
import time
from queue import Queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'cookie' : '你的cookie'
}


class Producer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            # 休息几秒钟
            time.sleep(random.randint(1, 3))
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, headers=headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='random_picture']//a//img")
        for img in imgs:
            # 过滤动图
            if img.get('class') == 'gif':
                continue

            # 获取图片url
            img_url = img.xpath(".//@data-backup")[0]
            if img_url.split('.')[-1] == 'gif':
                continue

            # 获取图片后缀
            suffix = os.path.splitext(img_url)[1]

            # 获取图片名称
            alt = img.xpath(".//@alt")[0]

            img_name = alt + suffix
            self.img_queue.put((img_url, img_name))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                return

            img = self.img_queue.get(block=True)
            url, filename = img
            with open("./images/"+filename, 'wb') as f:
                f.write(requests.get(url, timeout=30, headers=headers).content)
                f.close()
                print(filename + ' 下载完成！')


def main():
    # url队列
    page_queue = Queue(15)
    img_queue = Queue(20)
    page_queue.put('https://www.doutula.com/photo/list/')
    for x in range(2, 6):
        url = "https://www.doutula.com/photo/list/?page={}" .format(str(x))
        page_queue.put(url)

    for x in range(6):
        t = Producer(page_queue, img_queue)
        t.start()

    for x in range(6):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()








