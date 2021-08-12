#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
# coding:utf-8
import os
from PIL import Image

imgFolderPath = "C:\\Users\\xxx\\Downloads\\imgs"
fileList = os.listdir(imgFolderPath)
firstImgPath = os.path.join(imgFolderPath, fileList[0])
im = Image.open(firstImgPath)
images = []
for img in fileList[1:]:
    imgPath = os.path.join(imgFolderPath, img)
    images.append(Image.open(imgPath))
im.save('C:\\Users\\xxx\\Downloads\\imgs\\beauty.gif', save_all=True, append_images=images, loop=0, duration=500)
