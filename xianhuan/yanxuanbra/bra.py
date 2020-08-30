#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import requests
import time
import json

# 获取产品列表
def search_keyword(keyword):
    uri = 'https://you.163.com/xhr/search/search.json'
    query = {
        "keyword": keyword,
        "page": 1
    }
    try:
        res = requests.get(uri, params=query).json()
        result = res['data']['directly']['searcherResult']['result']
        product_id = []
        for r in result:
            product_id.append(r['id'])
        return product_id
    except:
        raise

# 获取评论
def details(product_id):
    url = 'https://you.163.com/xhr/comment/listByItemByTag.json'
    try:
        C_list = []
        for i in range(1, 100):
            query = {
                "itemId": product_id,
                "page": i,
            }
            res = requests.get(url, params=query).json()
            if not res['data']['commentList']:
                break
            print("爬取第 %s 页评论" % i)
            commentList = res['data']['commentList']
            C_list.extend(commentList)
            time.sleep(1)

        return C_list
    except:
        raise


product_id = search_keyword('文胸')
r_list = []
for p in product_id:
    r_list.extend(details(p))

with open('./comments.txt', 'w') as f:
    for r in r_list:
        try:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        except:
            print('出错啦')