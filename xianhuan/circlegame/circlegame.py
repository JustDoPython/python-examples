#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""
import pygame, random, sys, time

pygame.init()
screen = pygame.display.set_mode([600, 400])
screen.fill((255, 255, 255))
# 圆的半径
radius = [0] * 10
# 圆的半径增量
circleDelt = [0] * 10
# 圆是否存在,False代表该索引值下的圆不存在，True代表存在
circleExists = [False] * 10
# 圆的坐标x轴
circleX = [0] * 10
# 圆的坐标y轴
circleY = [0] * 10
# 颜色RGB值
RGBx = [0] * 10
RGBy = [0] * 10
RGBz = [0] * 10

while True:
    # 停顿0.1秒
    time.sleep(0.1)
    for event in pygame.event.get():
        # 鼠标按下
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 获取圆不存在的索引值
            num = circleExists.index(False)
            # 将该索引值的圆设置为存在
            circleExists[num] = True
            # 圆的半径设置为0
            radius[num] = 0
            # 获取鼠标坐标
            circleX[num], circleY[num] = pygame.mouse.get_pos()
            # 随机获取颜色值
            RGBx[num] = random.randint(0, 255)
            RGBy[num] = random.randint(0, 255)
            RGBz[num] = random.randint(0, 255)
            # 画圆
            pygame.draw.circle(screen, pygame.Color(RGBx[num], RGBy[num], RGBz[num]),
                               (circleX[num], circleY[num]), radius[num], 1)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in range(10):
        # 圆不存在则跳过循环
        if not circleExists[i]:
            pass
        else:
            # 随机圆的大小
            if radius[i] < random.randint(10, 50):
                # 圆的随机半径增量
                circleDelt[i] = random.randint(0, 5)
                radius[i] += circleDelt[i]
                # 画圆
                pygame.draw.circle(screen, pygame.Color(RGBx[i], RGBy[i], RGBz[i]),
                                   (circleX[i], circleY[i]), radius[i], 1)
            else:
                # 若圆已达到最大，这将该索引值的圆设置为不存在
                circleExists[i] = False
    pygame.display.update()
