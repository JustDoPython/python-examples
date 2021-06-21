#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import os
import easygui as g
import time


def get_macs():
    # 运行cmd控制窗口，输入“arp -a”，并将内容传递到res中
    res = os.popen("arp -a")
    # 读取res数据，转换为可读数据
    arps = res.read()
    print(arps)

    # 将获得的counts中的数据根据“换行符”来进行分割切片
    result = arps.split('\n')

    # 设一个空列表装ip
    ips = []
    # 设一个空列表装mac
    macs = []

    # 遍历
    for i in range(1, len(result)):
        # 获得列表中第idx个数据
        line = result[i]
        if ('Internet' in line) | ('' == line) | ('接口' in line):
            continue
        # 根据“ ”进行切片
        line_split = line.split(" ")
        index = 0
        for l in line_split:
            if l != '':
                index += 1
                if index == 1:
                    ips.append(l)
                elif index == 2:
                    macs.append(l)

    return ips, macs

# 老板的Mac地址
bossMac = "01-00-5e-0b-14-01"
sleep_time = 5
while 1 == 1:
    time.sleep(sleep_time)
    ips, macs = get_macs()
    is_come = 0
    for mac in macs:
        if mac == bossMac:
            is_come = 2
            # 如果boss来了，就隔5分钟扫描一次
            sleep_time = 300
            # 提示报警
            choice = g.msgbox(msg="有内鬼，终止交易！", title="OMG")
            break
    if is_come == 0:
        # 如果boss走了，就隔5秒钟扫描一次
        sleep_time = 5
        g.msgbox(msg="一切正常！", title="OMG")