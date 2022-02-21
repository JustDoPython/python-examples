#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import qrcode
import cv2

img = qrcode.make('https://www.zhihu.com/people/wu-huan-bu-san')
img.save('./pic.jpg')

d = cv2.QRCodeDetector()
val, _, _ = d.detectAndDecode(cv2.imread("pic.jpg"))
print("Decoded text is: ", val)

