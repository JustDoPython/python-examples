#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import requests
import json
import datetime
import lunarUtils

def get_data(year):
    url = 'https://staticwnl.tianqistatic.com/Public/Home/js/api/yjs/%d.js' % year
    response = requests.get(url)
    text = response.text
    start_str = 'lmanac["%d"] =' % year
    his_end_str = ';if(typeof(lmanac_2345)!="undefined"){lmanac_2345();}'
    cur_end_str = ';if(typeof(lmanac_2345)!="undefined"){lmanac_2345()};'
    cur_year = datetime.datetime.now().year
    jsonstr = text.replace(start_str, '')
    if cur_year == year:
        jsonstr = jsonstr.replace(cur_end_str, '')
    else:
        jsonstr = jsonstr.replace(his_end_str, '')

    return jsonstr


def choose_day(year, jsonstr):
    jobj = json.loads(jsonstr)
    for day in jobj.keys():
        y = jobj[day]['y']
        if '嫁娶' in y:
            dtime = datetime.datetime(year, int(day[1:3]), int(day[3:5]))
            # 获取农历日期
            ludar_date = lunarUtils.get_ludar_date(dtime)
            # 取得日，然后看是否是双数
            if ludar_date[2] % 2 == 0:
                print('公历日期：%s，农历日期：%s' % (day, ludar_date))

choose_day(2021, get_data(2021))