#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site : 
# @Describe:

# from ironman.nginx_log_data import province_data, \
#     line_legend, line_normal, line_spider, \
#     bar_legend, bar_normal, bar_spider, \
#     client_data, spider_data
from ironman.nginx_log_data import *

class SourceData:

    @property
    def china(self):
        return province_data

    @property
    def line(self):
        data = {
            '正常访问量': line_normal,
            # '爬虫访问量': line_normal,
            'legend': line_legend
        }
        return data

    @property
    def bar(self):
        data = {
            '正常访问量': bar_normal,
            # '爬虫访问量': bar_spider,
            'legend': bar_legend
        }
        return data

    @property
    def pie(self):
        return client_data

    # @property
    # def wordcloud(self):
    #     return spider_data
