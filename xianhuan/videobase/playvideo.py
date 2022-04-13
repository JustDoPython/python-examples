#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import cv2 as cv
cap = cv.VideoCapture('video.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if not ret:
        break
    cv.imshow('frame', frame)
    if cv.waitKey(25) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()