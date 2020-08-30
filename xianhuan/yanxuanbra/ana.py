#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import json
import pandas as pd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
import jieba
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import numpy as np
from os import path

size = ['XXL', 'XL', 'XS', 'S', 'M', 'L']

color = []
size1 = []
size2 = []
comments = []

with open("comments.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_obj = json.loads(line)
        comments.append(data_obj['content'])
        skuinfo = data_obj['skuInfo']
        # skuArr = skuinfo.split(",")
        for sku in skuinfo:
            if '颜色' in sku and '内裤' not in sku:
                color.append(sku.replace("颜色:", "").strip().replace("开扣", "").replace("套头", "").replace("文胸", "").replace("套装", "").replace("（薄杯）", "").replace("（厚杯）", ""))
            elif '尺码' in sku:
                is_size1 = False
                for s in size:
                    if s in sku:
                        is_size1 = True
                        size1.append(s)
                        break

                # 非SML这种定义尺寸的，就是简单罩杯定义的，同时去掉"适合75ABCD"这种定义的
                if not is_size1 and '适合' not in sku:
                    size2.append(sku.replace('尺码:', ""))

# 颜色可视化
df = pd.DataFrame(color, columns=['color'])
analyse_color = df['color'].value_counts()

bar = Bar()
bar.add_xaxis(analyse_color.index.values.tolist())
bar.add_yaxis("", analyse_color.values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
    title_opts=opts.TitleOpts(title="颜色分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
# bar.render_notebook()
bar.render('color.html')


# 尺码可视化
df2 = pd.DataFrame(size1, columns=['size'])
analyse_size = df2['size'].value_counts()

bar = Bar()
bar.add_xaxis(analyse_size.index.values.tolist())
bar.add_yaxis("", analyse_size.values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
    title_opts=opts.TitleOpts(title="尺寸分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render('size1.html')

df2 = pd.DataFrame(size2, columns=['size'])
analyse_size = df2['size'].value_counts()

bar = Bar()
bar.add_xaxis(analyse_size.index.values.tolist())
bar.add_yaxis("", analyse_size.values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
    title_opts=opts.TitleOpts(title="尺寸分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render('size2.html')



# 评论可视化
text = " ".join(comments)
def gen_wc_split_text(text='There is no txt', max_words=None, background_color=None,
                      font_path='/System/Library/Fonts/PingFang.ttc',
                      output_path='', output_name='',
                      mask_path=None, mask_name=None,
                      width=400, height=200, max_font_size=100, axis='off'):
    all_seg = jieba.cut(text, cut_all=False)
    split_text = ' '
    for seg in all_seg:
        split_text = split_text + seg + ' '

    # 设置一个底图
    mask = None
    if mask_path is not None:
        mask = np.array(Image.open(path.join(mask_path, mask_name)))

    wordcloud = WordCloud(background_color=background_color,
                          mask=mask,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          width=width,
                          height=height,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path=font_path)
    myword = wordcloud.generate(str(split_text))
    # 展示词云图
    plt.imshow(myword)
    plt.axis(axis)
    plt.show()

    # 保存词云图
    wordcloud.to_file(path.join(output_path, output_name))

gen_wc_split_text(text, output_name='comments_wc.png', output_path='./')
