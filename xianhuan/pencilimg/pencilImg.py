#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import cv2

# 读取 RGB 格式的美女图片
img = cv2.imread("mv5.jpg")
# 将 BGR 图像转为灰度模式
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 显示灰度图像
# cv2.imshow('grey', gray_img)
# cv2.waitKey(0)
# cv2.imwrite("./grey.jpg", gray_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
# 反转图像
inverted_img = 255 - gray_img

# 创建铅笔草图
blurred = cv2.GaussianBlur(inverted_img, (21, 21), 0)
inverted_blurred = 255 - blurred
cv2.imwrite("./inverted_blurred.jpg", inverted_blurred, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
pencil_sketch = cv2.divide(gray_img, inverted_blurred, scale=256.0)
# 显示图像
cv2.imshow("original", img)
cv2.imshow("pencil", pencil_sketch)
cv2.waitKey(0)




