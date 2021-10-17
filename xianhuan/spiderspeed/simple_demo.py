#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import time
import requests
from datetime import datetime


def fetch(url):
    r = requests.get(url)
    print(r.text)

start = datetime.now()

t1 = time.time()
for i in range(100):
    fetch('http://httpbin.org/get')

print('requests版爬虫耗时：', time.time() - t1)









