#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
from PIL import ImageEnhance, Image
#-*- coding: UTF-8 -*-

from PIL import Image
from PIL import ImageEnhance

#原始图像
image = Image.open('girl.jpeg')
image.show()

#亮度增强
enh_bri = ImageEnhance.Brightness(image)
brightness = 4
image_brightened = enh_bri.enhance(brightness)
image_brightened.show()

#色度增强
enh_col = ImageEnhance.Color(image)
color = 4
image_colored = enh_col.enhance(color)
image_colored.show()

#对比度增强
enh_con = ImageEnhance.Contrast(image)
contrast = 4
image_contrasted = enh_con.enhance(contrast)
image_contrasted.show()

#锐度增强
enh_sha = ImageEnhance.Sharpness(image)
sharpness = 4
image_sharped = enh_sha.enhance(sharpness)
image_sharped.show()
