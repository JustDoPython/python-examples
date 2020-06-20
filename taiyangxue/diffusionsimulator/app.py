# 引入pygame和sys模块
import pygame, sys
import math
from pygame.locals import *
import time
import people

WIDTH = 500
HEIGHT = 500

RADIUS = 25
POINT_RADIUS = 5

BLACK = (0,0,0)
WHITE = (255,255,255)
PINK = (255,192,203)
RED = (255,0,0)

# 初始化pygame
pygame.init()

# 设置窗口与窗口标题
windowSurface = pygame.display.set_mode((WIDTH,HEIGHT),0,8)
pygame.display.set_caption('疫情模拟')

# 初始化人群
p = people.People(600, 1)

COLORS = [BLACK, PINK, RED]

# 事件循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    windowSurface.fill(WHITE)  # 设置画布背景 起到擦除的作用

    for i in range(len(p._status)):  # 健康
        x_point = p._people[i][0]
        y_point = p._people[i][1]
        pygame.draw.circle(windowSurface,COLORS[p._status[i]],(int(x_point), int(y_point)), POINT_RADIUS)

    # 绘制窗口到屏幕上
    pygame.display.update()
    time.sleep(0.1)
    p.update()