#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/27 14:06
# @Author : way
# @Site : 
# @Describe: 通过 ip 获取所在省份

import sys
import json
import requests
import os

ak = "<换成你的ak>" # 百度 ak 自行申请 http://lbsyun.baidu.com/index.php?title=webapi/ip-api

ipCache = {}
if os.path.exists("ip_cache.txt"):
    with open("ip_cache.txt", "r") as f:
        data = f.readline()
        while data:
            ip, province = data.strip().split("\t")
            ipCache[ip] = province
            data = f.readline()

def ip2province(ip):
    province = ipCache.get(ip, None)
    if province is None:
        url = f"https://api.map.baidu.com/location/ip?ak={ak}&ip={ip}&coor=bd09ll"
        try:
            province = json.loads(requests.get(url).text)['address'].split('|')[1]
            ipCache[ip] = province
            # 这里就需要写入
            with open("ip_cache.txt","a") as f:
                f.write(ip + "\t" + province + "\n")
            return province
        except Exception as e:
            return "未知"
    else:
        return province

if __name__ == '__main__':
    for line in sys.stdin:
        cols = line.replace('\n', '').split('\t')
        print(cols)
        cols = [ip2province(cols[0]), cols[0]]
        sys.stdout.write('\t'.join(cols) + '\n')
