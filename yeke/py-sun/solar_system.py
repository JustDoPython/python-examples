import sys
import math
import pygame
from pygame.locals import *

pygame.init()
WHITE =(255, 255, 255)
SILVER = (192, 192, 192)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SandyBrown = (244, 164, 96)
PaleGodenrod = (238, 232, 170)
PaleVioletRed = (219, 112, 147)
Thistle = (216, 191, 216)
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("太阳系")
# 创建时钟(控制游戏循环频率)
clock = pygame.time.Clock()
# 定义三个空列表
pos_v = pos_e = pos_mm = []
# 地球、月球等行星转过的角度
roll_v = roll_e = roll_m = 0
roll_3 = roll_4 = roll_5 = roll_6 = roll_7 = roll_8 = 0
# 太阳的位置（中心）
position = size[0] // 2, size[1] // 2

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            # 背景颜色为黑色
    screen.fill(BLACK)
    # 画太阳
    pygame.draw.circle(screen, YELLOW, position, 60, 0)
    # 画地球
    roll_e += 0.01  # 假设地球每帧公转 0.01 pi
    pos_e_x = int(size[0] // 2 + size[1] // 6 * math.sin(roll_e))
    pos_e_y = int(size[1] // 2 + size[1] // 6 * math.cos(roll_e))
    pygame.draw.circle(screen, BLUE, (pos_e_x, pos_e_y), 15, 0)
    # 地球的轨迹线
    pos_e.append((pos_e_x, pos_e_y))
    if len(pos_e) > 255:
        pos_e.pop(0)
    for i in range(len(pos_e)):
        pygame.draw.circle(screen, SILVER, pos_e[i], 1, 0)
    # 画月球
    roll_m += 0.1
    pos_m_x = int(pos_e_x + size[1] // 20 * math.sin(roll_m))
    pos_m_y = int(pos_e_y + size[1] // 20 * math.cos(roll_m))
    pygame.draw.circle(screen, WHITE, (pos_m_x, pos_m_y), 8, 0)
    # 月球的轨迹线
    pos_mm.append((pos_m_x, pos_m_y))
    if len(pos_mm) > 255:
        pos_mm.pop(0)
    for i in range(len(pos_mm)):
        pygame.draw.circle(screen, SILVER, pos_mm[i], 1, 0)
    # 画金星
    roll_v += 0.015
    pos_v_x = int(size[0] // 2 + size[1] // 3 * math.sin(roll_v))
    pos_v_y = int(size[1] // 2 + size[1] // 3 * math.cos(roll_v))
    pygame.draw.circle(screen, RED, (pos_v_x, pos_v_y), 20, 0)
    # 金星的轨迹线
    pos_v.append((pos_v_x, pos_v_y))
    if len(pos_v) > 255:
        pos_v.pop(0)
    for i in range(len(pos_v)):
        pygame.draw.circle(screen, SILVER, pos_v[i], 1, 0)
    # 其他几个行星
    roll_3 += 0.03
    pos_3_x = int(size[0] // 2 + size[1] // 3.5 * math.sin(roll_3))
    pos_3_y = int(size[1] // 2 + size[1] // 3.5 * math.cos(roll_3))
    pygame.draw.circle(screen, GREEN, (pos_3_x, pos_3_y), 20, 0)
    roll_4 += 0.04
    pos_4_x = int(size[0] // 2 + size[1] // 4 * math.sin(roll_4))
    pos_4_y = int(size[1] // 2 + size[1] // 4 * math.cos(roll_4))
    pygame.draw.circle(screen, SandyBrown, (pos_4_x, pos_4_y), 20, 0)
    roll_5 += 0.05
    pos_5_x = int(size[0] // 2 + size[1] // 5 * math.sin(roll_5))
    pos_5_y = int(size[1] // 2 + size[1] // 5 * math.cos(roll_5))
    pygame.draw.circle(screen, PaleGodenrod, (pos_5_x, pos_5_y), 20, 0)
    roll_6 += 0.06
    pos_6_x = int(size[0] // 2 + size[1] // 2.5 * math.sin(roll_6))
    pos_6_y = int(size[1] // 2 + size[1] // 2.5 * math.cos(roll_6))
    pygame.draw.circle(screen, PaleVioletRed, (pos_6_x, pos_6_y), 20, 0)
    roll_7 += 0.07
    pos_7_x = int(size[0] // 2 + size[1] // 4.5 * math.sin(roll_7))
    pos_7_y = int(size[1] // 2 + size[1] // 4.5 * math.cos(roll_7))
    pygame.draw.circle(screen, Thistle, (pos_7_x, pos_7_y), 20, 0)
    roll_8 += 0.08
    pos_8_x = int(size[0] // 2 + size[1] // 5.5 * math.sin(roll_8))
    pos_8_y = int(size[1] // 2 + size[1] // 5.5 * math.cos(roll_8))
    pygame.draw.circle(screen, WHITE, (pos_8_x, pos_8_y), 20, 0)
    # 刷新
    pygame.display.flip()
    # 数值越大刷新越快，小球运动越快
    clock.tick(40)