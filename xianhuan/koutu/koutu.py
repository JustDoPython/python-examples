#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import os, paddlehub as hub
huseg = hub.Module(name='deeplabv3p_xception65_humanseg') # 加载模型
path = './imgs/' # 文件目录
files = [path + i for i in os.listdir(path)] # 获取文件列表
results = huseg.segmentation(data={'image': files}) # 抠图
