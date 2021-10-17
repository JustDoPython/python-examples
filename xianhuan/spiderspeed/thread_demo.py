#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import threading
import time
import requests


def fetch():
    r = requests.get('http://httpbin.org/get')
    print(r.text)

t1 = time.time()

t_list = []
for i in range(100):
    t = threading.Thread(target=fetch, args=())
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()

print("多线程版爬虫耗时：", time.time() - t1)