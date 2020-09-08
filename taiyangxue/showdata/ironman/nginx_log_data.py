#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/27 19:32
# @Author : way
# @Site : 
# @Describe:

import pandas as pd

filepath = "data.xlsx"#"分析结果.xlsx"

df2 = pd.read_excel(filepath, sheet_name='省份', header=None)

province_data = [{'name': row[0].strip(), 'value': row[1]} for row in df2.values]
# print(province_data)

df3 = pd.read_excel(filepath, sheet_name='按时', header=None)
line_legend = [row[0] for row in df3.values]
line_normal = [row[1] for row in df3.values]
# line_spider = [row[2] for row in df3.values if row[0]=='Spider']
# print(line_legend)
# print(line_normal)
# print(line_spider)

# df3 = pd.read_excel(filepath, sheet_name='按天', header=None)
# bar_legend = [row[1].strftime('%Y%m%d') for row in df3.values if row[0]=='Normal']
# bar_normal = [row[2] for row in df3.values if row[0]=='Normal']
# bar_spider = [row[2] for row in df3.values if row[0]=='Spider']
# print(bar_legend)
# print(bar_normal)
# print(bar_spider)

df3 = pd.read_excel(filepath, sheet_name='客户端', header=None)
client_data = [{'name': row[0].strip(), 'value': row[1]} for row in df3.values]
# print(client_data)

# df3 = pd.read_excel(filepath, sheet_name='爬虫', header=None)
# spider_data = [{'name': row[0].strip(), 'value': row[1]} for row in df3.values]
# print(spider_data)