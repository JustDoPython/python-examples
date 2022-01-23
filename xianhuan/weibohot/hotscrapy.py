#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/01/11 11:15:24
@Author  :   闲欢 
@Desc    :   爬取微博历史热榜
'''

import datetime
import pandas as pd
import requests
import time
import random
import json


headers = {
        "Host": "google-api.zhaoyizhe.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

def scrapy(date):
    print('开始爬取%s' % date)
    url = 'https://google-api.zhaoyizhe.com/google-api/index/mon/sec?date=%s' % date
    try:
        time.sleep(random.randint(1, 3))
        res = requests.get(url, headers=headers).json()
        result = res['data']
        return result
    except Exception as err:
        print(err)
        return None


def get_date_list(startdate, enddate, freq='1D', dformat='%Y-%m-%d'):
    tm_rng = pd.date_range(startdate, enddate, freq=freq)
    return [x.strftime(dformat) for x in tm_rng]


hot_list = []
date_list = get_date_list('2021-01-01', '2021-12-31')
# print(date_list)
for d in date_list:
    result = scrapy(d)
    if result:
        hot_list.extend(result)

with open(r"c:\pworkspace\mypy\pythontech\weibohot\comments.txt",  'w', encoding='utf-8') as f:
    for r in hot_list:
        try:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        except Exception as err:
            print(err)
            print('出错啦')