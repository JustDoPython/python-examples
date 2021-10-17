#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import requests
import time
import multiprocessing
from multiprocessing import Pool

MAX_WORKER_NUM = multiprocessing.cpu_count()

def fetch():
    r = requests.get('http://httpbin.org/get')
    print(r.text)

if __name__ == '__main__':
    t1 = time.time()
    p = Pool(MAX_WORKER_NUM)
    for i in range(100):
        p.apply_async(fetch, args=())
    p.close()
    p.join()

    print('多进程爬虫耗时：', time.time() - t1)