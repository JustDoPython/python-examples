# -*- coding: utf-8 -*-
import json, re, requests, ssl
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

url_list = []
num_list = []
brand_dict = {}


def get_brand_id(num):
    x = 'https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-%s-x-x' % num
    rep = requests.get(x, timeout=10)
    soup = BeautifulSoup(rep.text, 'html.parser')
    condition = soup.find_all('span', class_='layout_label__1qfS8')
    # 当num大于500时，有可能没这个品牌，condition[5]会报错
    try:
        s = condition[5].next_sibling.a.text
        print('s111', s)
        url_list.append(x)
    except Exception as e:
        pass

    for span in condition:
        if span.string == '已选条件':
            print('ok')
            brand_dict[s] = num
            num_list.append(num)


pool = ThreadPool(10)
pool.map(get_brand_id, [i for i in range(1, 1000)])
print(num_list)
print(brand_dict)
print(url_list)
