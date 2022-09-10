# 导入所需模块
import random
import pygame

# pygame初始化 
pygame.init()

# 设置主屏窗口
screen = pygame.display.set_mode((600, 800))

# 设置游戏名称
pygame.display.set_caption("明月几时有")

# 加载背景
bg_menu = pygame.image.load("pic/bg1.jpg")
bg_game = pygame.image.load("pic/bg2.jpg")
word_menu = pygame.image.load("pic/word.png")

# 加载UI
target = pygame.image.load("pic/target.png")
wrong = pygame.image.load("pic/wrong.png")
player = pygame.image.load("pic/player.png")
btn = pygame.image.load("pic/button.png")

# 定义文字，初始化变量
score_word = "分数"
time_word = "机会"
end_word = "你的分数是{}，中秋快乐！"

font = pygame.font.SysFont("Microsoft YaHei", 40)

score = 0
score_num = font.render(str(score), True, (255, 255, 255))
time = 4
time_num = font.render(str(time), True, (255, 255, 255))

time_text = font.render(time_word, True, (255, 255, 255))
score_text = font.render(score_word, True, (255, 255, 255))
end_text = font.render(end_word.format(score), True, (255, 255, 255))
 
now_pos = 0
speed1 = 1
speed2 = 1.5
tar_pos = []
wro_pos = []


# 控制月饼密度
for i in range(0, 8):
    tar_pos.append([random.randint(50, 550),(i - 1) * 100])
 
# 控制树枝密度
for i in range(0, 2):
    wro_pos.append([random.randint(50, 550),(i - 1) * 300])
 
 
# 按钮类
class Button(object):
    # 初始化
    def __init__(self, btn, position):
        self.btn = btn
        self.position = position
        
    def show(self):
        weight, height = self.btn.get_size()
        x_pos, y_pos = self.position
        screen.blit(self.btn, (x_pos-weight/2, y_pos-height/2))

    # 判断是否按下
    def click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            point_x, point_y = pygame.mouse.get_pos()
            x_pos, y_pos = self.position
            weight, height = self.btn.get_size()
            ok_x = x_pos-weight/2 < point_x < x_pos+weight/2
            ok_y = y_pos-height/2 < point_y < y_pos+height/2
            if ok_x and ok_y:
                return True

button = Button(btn, (300, 420))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    # 初始菜单
    screen.blit(bg_menu, (0, 0))
    screen.blit(word_menu, (0, -70))
    button.show()
    if button.click():
        time = 3
        score = 0
        score_num = font.render(str(score), True, (255, 255, 255))
        time_num = font.render(str(time), True, (255, 255, 255))

    # 开始游戏
    if time > 0 and time < 4 and score >= 0:
        screen.blit(bg_game, (0, 0))
        screen.blit(time_text, (50, 50))
        screen.blit(time_num, (170, 50))
        screen.blit(score_text, (50, 100))
        screen.blit(score_num, (170, 100))
        screen.blit(player, (now_pos, 550))

        # 速度变化
        if score <= 30:
            speed1 = 0.8
            speed2 = 1.2
        elif score <= 60:
            speed1 = 1
            speed2 = 1.5
        elif score <= 90:
            speed1 = 1.2
            speed2 = 1.8
        elif score <= 120:
            speed1 = 1.4
            speed2 = 2.1
        elif score <= 150:
            speed1 = 1.8
            speed2 = 2.7
        elif score <= 200:
            speed1 = 2
            speed2 = 3
        elif score <= 250:
            speed1 = 3
            speed2 = 4.5
        else:
            speed1 = 4
            speed2 = 6

        # 月饼运动路线
        for i in range(len(tar_pos)):
            screen.blit(pygame.transform.scale(target, (50, 50)), (tar_pos[i][0], tar_pos[i][1] - 800))
            tar_pos[i][1] += speed1
            if tar_pos[i][1] > 1600:
                tar_pos[i][1] = 800
                tar_pos[i][0] = random.randint(50, 550)
                score -= 2
                score_num = font.render(str(score), True, (255, 255, 255))
            # 边界判定
            if tar_pos[i][0] + 50 > now_pos and tar_pos[i][0]  < now_pos + 75 and tar_pos[i][1] >= 1300 and tar_pos[i][1] <= 1500:
                tar_pos[i][1] = 800
                tar_pos[i][0] = random.randint(50, 550)
                score += 10
                score_num = font.render(str(score), True, (255, 255, 255))

        # 树枝运动路线
        for i in range(len(wro_pos)):
            screen.blit(pygame.transform.scale(wrong, (50, 50)), (wro_pos[i][0], wro_pos[i][1] - 800))
            wro_pos[i][1] += speed2
            if wro_pos[i][1] > 1600:
                wro_pos[i][1] = 800
                wro_pos[i][0] = random.randint(50, 550)
            # 边界判定
            if wro_pos[i][0] + 50 > now_pos and wro_pos[i][0] < now_pos + 75 and wro_pos[i][1] >= 1300 and wro_pos[i][1] <= 1500:
                wro_pos[i][1]= 800
                wro_pos[i][0] = random.randint(50, 550)
                time -= 1
                time_num = font.render(str(time), True, (255, 255, 255))
 
        # 角色移动
        if event.type == pygame.MOUSEMOTION:
            move_x, move_y = pygame.mouse.get_pos()
            now_pos = move_x - 75
        if now_pos < 0:
            now_pos = 0
        if now_pos > 600:
            now_pos = 525
 
    # 重新开始游戏
    if time == 0 or score < 0:
        # 初始化游戏
        now_pos = 0
        speed = 1
        # 月饼运动路线
        for i in range(len(tar_pos)):
            tar_pos[i][0] = random.randint(50, 550)
            tar_pos[i][1] = (i - 1) * 100
        # 树枝运动路线
        for i in range(len(wro_pos)):
            wro_pos[i][0] = random.randint(50, 550)
            wro_pos[i][1] = (i - 1) * 300
        end_text = font.render(end_word.format(score), True, (255, 255, 255))
        screen.blit(bg_menu, (0, 0))
        screen.blit(end_text, (50, 220))
        button.show()
        # 点击按钮重开
        if button.click():
            time = 3
            score = 0
            score_num = font.render(str(score), True, (255, 255, 255))
            
    pygame.display.update()