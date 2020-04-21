import pygame, random
from sys import exit
from pygame.locals import *
from pl_model import *

# 设置屏幕的宽度
SCREEN_WIDTH = 450
# 设置屏幕的高度
SCREEN_HEIGHT = 600
# 初始化窗口
pygame.init()
# 设置窗口标题
pygame.display.set_caption("飞机大战")
# 设置屏幕大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# 隐藏光标
pygame.mouse.set_visible(False)
# 设置背景
bg = pygame.image.load("resources/image/bg.png")
# 设置游戏结束的图片
bg_game_over = pygame.image.load("resources/image/bg_game_over.png")
# 加载飞机资源图片
img_plane = pygame.image.load("resources/image/shoot.png")
img_start = pygame.image.load("resources/image/start.png")
img_pause = pygame.image.load("resources/image/pause.png")
img_icon = pygame.image.load("resources/image/plane.png").convert_alpha()
# 顺便设置窗口
pygame.display.set_icon(img_icon)
# 初始化飞机区域
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
# 玩家爆炸图片
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# 初始化位置
player_pos = [200, 450]
# 生成玩家类
player = Player(img_plane, player_rect, player_pos)
# 设置子弹框
bullet_rect = pygame.Rect(1004, 987, 9, 21)
# 加载子弹图片
bullet_img = img_plane.subsurface(bullet_rect)
# 设置敌人框
enemy_rect = pygame.Rect(534, 612, 57, 43)
# 设置敌人图片
enemy_img = img_plane.subsurface(enemy_rect)
# 设置敌人被击图片
enemy_explosion_imgs = []
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))
# 设置敌机精灵组
enemies = pygame.sprite.Group()
# 设置敌机被击精灵组
enemies_explosion = pygame.sprite.Group()
# 设置射击频率
shoot_frequency = 0
# 设置敌机频率
enemy_frequency = 0
# 设置玩家被击的图片顺序
player_explosion_index = 16
score = 0
running = True
is_pause = False
is_game_over = False
clock = pygame.time.Clock()

# 开始游戏循环
while running:
    # 设置游戏帧率为 60
    clock.tick(60)
    if not is_pause and not is_game_over:
        if not player.is_hit:
            # 设置连续射击,因为每秒 60 帧,15/60=0.25 秒发一次子弹
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            # 当设置的射击频率大于 15，置零
            if shoot_frequency >= 15:
                shoot_frequency = 0
        # 控制生成敌机的频率
        if enemy_frequency % 50 == 0:
            # 设置敌机的出现的位置
            enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
            enemy = Enemy(enemy_img, enemy_explosion_imgs, enemy_pos)
            enemies.add(enemy)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0
        # 控制子弹的显示运行
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # 控制敌机的运行
        for enemy in enemies:
            enemy.move()
            # 判断敌机是否与玩家飞机碰撞
            if pygame.sprite.collide_circle(enemy, player):
                enemies_explosion.add(enemy)
                enemies.remove(enemy)
                player.is_hit = True
                # 设置玩家的飞机被毁
                is_game_over = True
            # 判断敌机是否在界面
            if enemy.rect.top < 0:
                enemies.remove(enemy)
        # 设置敌机与玩家的飞机子弹相碰时，返回被击的敌机实例
        enemy_explosion = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
        for enemy in enemy_explosion:
            enemies_explosion.add(enemy)
    # 绘制屏幕
    screen.fill(0)
    # 加入背景图片
    screen.blit(bg, (0, 0))
    # 添加玩家飞机图片到屏幕
    if not player.is_hit:
        screen.blit(player.image[int(player.img_index)], player.rect)
        player.img_index = shoot_frequency / 8
    else:
        if player_explosion_index > 47:
            is_game_over = True
        else:
            player.img_index = player_explosion_index / 8
            screen.blit(player.image[int(player.img_index)], player.rect)
            player_explosion_index += 1
    # 敌机被子弹击中的效果显示
    for enemy in enemies_explosion:
        if enemy.explosion_index == 0:
            pass
        if enemy.explosion_index > 7:
            enemies_explosion.remove(enemy)
            score += 100
            continue
        # 敌机被击时显示图片
        screen.blit(enemy.explosion_img[int(enemy.explosion_index / 2)], enemy.rect)
        enemy.explosion_index += 1
    # 显示子弹
    player.bullets.draw(screen)
    # 显示敌机
    enemies.draw(screen)
    # 分数的显示效果
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    # 设置文字框
    text_rect = score_text.get_rect()
    # 放置文字的位置
    text_rect.topleft = [20, 10]
    # 显示出分数
    screen.blit(score_text, text_rect)
    left, middle, right = pygame.mouse.get_pressed()
    # 暂停游戏
    if right == True and not is_game_over:
        is_pause = True
    if left == True:
        # 重置游戏
        if is_game_over:
            is_game_over = False
            player_rect = []
            player_rect.append(pygame.Rect(0, 99, 102, 126))
            player_rect.append(pygame.Rect(165, 360, 102, 126))
            player_rect.append(pygame.Rect(165, 234, 102, 126))
            player_rect.append(pygame.Rect(330, 624, 102, 126))
            player_rect.append(pygame.Rect(330, 498, 102, 126))
            player_rect.append(pygame.Rect(432, 624, 102, 126))
            player = Player(img_plane, player_rect, player_pos)
            bullet_rect = pygame.Rect(1004, 987, 9, 21)
            bullet_img = img_plane.subsurface(bullet_rect)
            enemy_rect = pygame.Rect(534, 612, 57, 43)
            enemy_img = img_plane.subsurface(enemy_rect)
            enemy_explosion_imgs = []
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
            enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))
            enemies = pygame.sprite.Group()
            enemies_explosion = pygame.sprite.Group()
            score = 0
            shoot_frequency = 0
            enemy_frequency = 0
            player_explosion_index = 16
        # 继续游戏
        if is_pause:
            is_pause = False
    # 游戏结束
    if is_game_over:
        font = pygame.font.SysFont("微软雅黑", 48)
        text = font.render("Score: " + str(score), True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 70
        # 显示游戏结束画面
        screen.blit(bg_game_over, (0, 0))
        # 显示分数
        screen.blit(text, text_rect)
        font = pygame.font.SysFont("微软雅黑", 40)
        text = font.render("Press Left Mouse to Restart", True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 150
        screen.blit(text, text_rect)
    # 刷新屏幕
    pygame.display.update()
    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not is_pause and not is_game_over:
        key = pygame.key.get_pressed()
        if key[K_w] or key[K_UP]:
            player.moveUp()
        if key[K_s] or key[K_DOWN]:
            player.moveDown()
        if key[K_a] or key[K_LEFT]:
            player.moveLeft()
        if key[K_d] or key[K_RIGHT]:
            player.moveRight()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # 刷新屏幕
    pygame.display.update()
