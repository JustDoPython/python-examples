#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

import cv2
from PIL import ImageEnhance,Image
import numpy as np

def img_enhance(image, brightness=1, color=1,contrast=1,sharpness=1):
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(image)
    if brightness:
        image = enh_bri.enhance(brightness)

    # 色度增强
    enh_col = ImageEnhance.Color(image)
    if color:
        image = enh_col.enhance(color)

    # 对比度增强
    enh_con = ImageEnhance.Contrast(image)
    if contrast:
        image = enh_con.enhance(contrast)

    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(image)
    if sharpness:
        image = enh_sha.enhance(sharpness)

    return image


cap = cv2.VideoCapture('C:\\xxx.mp4')
success, _ = cap.read()
# 分辨率-宽度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# 分辨率-高度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 总帧数
frame_counter = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_writer = cv2.VideoWriter('C:\\result.mp4', cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 15, (width, height), True)

while success:
    success, img1 = cap.read()
    try:
        image = Image.fromarray(np.uint8(img1))  # 转换成PIL可以处理的格式
        img_enhanced = img_enhance(image, 2, 2, 2, 3)
        video_writer.write(np.asarray(img_enhanced))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        break


cap.release()
video_writer.release()
cv2.destroyAllWindows()