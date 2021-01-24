# coding:utf-8
import random
import time

import pygame

W = 600
H = 500

class Ball:

    x = None  # x坐标
    y = None  # y坐标
    speed_x = None  # x方向的速度
    speed_y = None  # y方向的速度
    radius = None  # 半径
    color = None  # 颜色

    def __init__(self, x, y, speed_x, speed_y, radius, color):
        """
        初始化
        :param x: X坐标
        :param y: Y坐标
        :param speed_x: X轴方向速度
        :param speed_y: Y轴方向速度
        :param radius: 半径
        :param color: 颜色
        """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        """
        绘制小球
        :param screen: 窗口
        :return:
        """
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius)


    def move(self, screen):
        """
        小球移动
        :param screen: 窗口
        :return:
        """
        self.x += self.speed_x
        self.y += self.speed_y

        # 左右边界
        if self.x > W - self.radius or self.x < self.radius:
            self.speed_x = -self.speed_x

        # 上下边界
        if self.y > H - self.radius or self.y < self.radius:
            self.speed_y = -self.speed_y
        # 移动频率
        time.sleep(0.001)
        self.draw(screen)


class Player:

    radius = None
    color = None
    x = 1000
    y = 1000

    def __init__(self, radius, color):
        """
        初始化
        :param radius: 半径
        :param color: 颜色
        """
        self.radius = radius
        self.color = color

    def move(self, screen):
        """
        大球移动
        :return:
        """
        # 鼠标检测
        if pygame.mouse.get_focused():
            # 获取光标位置,
            x, y = pygame.mouse.get_pos()

            mouse = pygame.mouse.get_pressed()

            pygame.draw.circle(screen, self.color, [x, y], self.radius)
            self.x = x
            self.y = y

balls = []
def create_ball(screen):
    """
    创建小球
    :param screen:
    :return:
    """
    x = random.randint(0, W)
    y = random.randint(0, H)
    speed_x = random.randint(-5, 5)
    speed_y = random.randint(-5, 5)
    r = 3
    color = 'white'
    b = Ball(x, y, speed_x, speed_y, r, color)

    balls.append(b)

    b.draw(screen)

def show_text(screen, text, pos, color, font_bold=False, font_size=18, font_italic=False):
    """
    显示文字
    :param screen: 窗口
    :param text: 文字
    :param pos: 坐标
    :param color: 颜色
    :param font_bold: 是否粗体
    :param font_size: 大小
    :param font_italic: 是否斜体
    :return:
    """
    cur_font = pygame.font.SysFont('Courier', font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text, 1, color)
    screen.blit(text_fmt, pos)

def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

def main():
    # 初始化pygame模块
    pygame.init()
    # 设置窗口大小
    screen = pygame.display.set_mode((W,H))
    # 设置窗口标题
    pygame.display.set_caption('是男人就坚持100秒')

    for i in range(0, 10):
       create_ball(screen)

    p = Player(10, 'red')
    text_time = "TIME:%.3d" % (time.perf_counter())

    is_loop = True
    while is_loop:
        # 重绘屏幕
        screen.fill((0))

        p.move(screen)

        for ball in balls:
            ball.move(screen)
            if abs(p.x - ball.x) < 13 and abs(p.y - ball.y) < 13:
                is_loop = False
                break

        # 刷新显示
        text_time = "TIME:%.3d" % (time.perf_counter())
        show_text(screen, text_time, (500, 40), (0, 255, 0), True)
        pygame.display.update()

        close()

    while True:
        close()
        show_text(screen, "Game over!", (120, 180), "green", True, 60)
        show_text(screen, text_time, (220, 270), "green", True, 30)

        pygame.display.update()


if __name__ == '__main__':
    main()
