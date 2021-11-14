#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

# coding:utf-8
import time, threading
from datetime import datetime
from PIL import ImageGrab
import numpy as np
from cv2.cv2 import VideoCapture, VideoWriter_fourcc, VideoWriter, cvtColor, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, \
    CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, COLOR_RGB2BGR
from pynput import keyboard


# 录入视频
def video_record(sttime):
    global name
    # 当前的时间（当文件名）
    name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 获取当前屏幕
    screen = ImageGrab.grab()
    # 获取当前屏幕的大小
    width, high = screen.size
    # MPEG-4编码,文件后缀可为.avi .asf .mov等
    fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D')
    # （文件名，编码器，帧率，视频宽高）
    video = VideoWriter('%s.avi' % name, fourcc, 15, (width, high))
    print(str(sttime) + '秒后开始录制----')
    time.sleep(int(sttime))
    print('开始录制!')
    global start_time
    start_time = time.time()
    while True:
        if flag:
            print("录制结束！")
            global final_time
            final_time = time.time()
            # 释放
            video.release()
            break
        # 图片为RGB模式
        im = ImageGrab.grab()
        # 转为opencv的BGR模式
        imm = cvtColor(np.array(im), COLOR_RGB2BGR)
        # 写入
        video.write(imm)



# 监听按键
def on_press(key):
    global flag
    if key == keyboard.Key.esc:
        flag = True
        # 返回False，键盘监听结束！
        return False



# 视频信息
def video_info():
    # 记得文件名加格式不要错！
    video = VideoCapture('%s.avi' % name)
    fps = video.get(CAP_PROP_FPS)
    count = video.get(CAP_PROP_FRAME_COUNT)
    size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
    print('帧率=%.1f' % fps)
    print('帧数=%.1f' % count)
    print('分辨率', size)
    print('视频时间=%.3f秒' % (int(count) / fps))
    print('录制时间=%.3f秒' % (final_time - start_time))
    print('推荐帧率=%.2f' % (fps * ((int(count) / fps) / (final_time - start_time))))


if __name__ == '__main__':
    flag = False
    print("工具使用：输入1-9秒必须为整数的延迟时间，点击esc按钮结束录屏")
    sstime = input("请输入多少秒后开始录制(1-9秒)必须为整数：", )
    th = threading.Thread(target=video_record, args=sstime)
    th.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    # 等待视频释放过后
    time.sleep(1)
    video_info()
