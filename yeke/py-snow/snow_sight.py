import pygame
import random

# 初始化 pygame
pygame.init()
# 设置屏幕宽高，根据背景图调整
bg_img = "bg.jpeg"
bg_size = (900, 500)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("雪景图")
bg = pygame.image.load(bg_img)
# 雪花列表
snow_list = []
for i in range(150):
    x_site = random.randrange(0, bg_size[0])   # 雪花圆心位置
    y_site = random.randrange(0, bg_size[1])   # 雪花圆心位置
    X_shift = random.randint(-1, 1)         # x 轴偏移量
    radius = random.randint(4, 6)           # 半径和 y 周下降量
    snow_list.append([x_site, y_site, X_shift, radius])
# 创建时钟对象
clock = pygame.time.Clock()
# 添加音乐
track = pygame.mixer.music.load('my.mp3')  # 加载音乐文件
pygame.mixer.music.play() # 播放音乐流
pygame.mixer.music.fadeout(600000)  # 设置音乐结束时间
done = False
while not done:
    # 消息事件循环，判断退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.blit(bg, (0, 0))
    # 雪花列表循环
    for i in range(len(snow_list)):
        # 绘制雪花，颜色、位置、大小
        pygame.draw.circle(screen, (255, 255, 255), snow_list[i][:2], snow_list[i][3] - 3)
        # 移动雪花位置（下一次循环起效）
        snow_list[i][0] += snow_list[i][2]
        snow_list[i][1] += snow_list[i][3]
        # 如果雪花落出屏幕，重设位置
        if snow_list[i][1] > bg_size[1]:
            snow_list[i][1] = random.randrange(-50, -10)
            snow_list[i][0] = random.randrange(0, bg_size[0])
    # 刷新屏幕
    pygame.display.flip()
    clock.tick(20)
# 退出
pygame.quit()