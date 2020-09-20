#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import pandas as pd
import os

result = pd.DataFrame()

for name in os.listdir("./tables"):
    try:
        df = pd.read_excel("./tables/" + name)
        df['销售额'] = df['访客数'] * df['转化率'] * df['客单价']
        df_sum = df.groupby('品牌')['销售额'].sum().reset_index()
        result = pd.concat([result, df_sum])
    except:
        print(name)
        pass

final = result.groupby('品牌')['销售额'].sum().reset_index().sort_values('销售额', ascending=False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(final.head())







