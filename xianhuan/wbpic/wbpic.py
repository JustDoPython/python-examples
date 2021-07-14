#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import requests
import re
import os
import time
cookie = {
    'Cookie': 'your cookie'
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4144.2 Safari/537.36'
}
get_order = input('是否启动程序? yes or no:   ')
number = 1
store_path = 'your path'
while True:
    if get_order != 'no':
        print('抓取中......')  # 下面的链接填写微博搜索的链接
        url = f'https://s.weibo.com/weibo?q=%23%E5%B0%91%E5%A5%B3%E5%86%99%E7%9C%9F%23&wvr=6&b=1&Refer=SWeibo_box&page={number}'
        response = requests.get(url, cookies=cookie)
        result = response.text
        print(result)
        detail = re.findall('data="uid=(.*?)&mid=(.*?)&pic_ids=(.*?)">', result)
        for part in detail:
            uid = part[0]
            mid = part[1]
            pids = part[2]
            for picid in pids.split(','):
                url_x = f'https://wx1.sinaimg.cn/large/%s.jpg'%picid  # 这里就是大图链接了
                response_photo = requests.get(url_x, headers=header)
                file_name = url_x[-10:]
                if not os.path.exists(store_path+uid):
                    os.mkdir(store_path+uid)
                with open(store_path+uid + '/' + file_name, 'ab') as f:  # 保存文件
                    f.write(response_photo.content)
                    time.sleep(0.5)
        print('获取完毕')
        get_order = input('是否继续获取下一页? Y:yes N:no:   ')
        if get_order != 'no':
            number += 1
        else:
            print('程序结束')
            break
    else:
        print('程序结束')
        break
