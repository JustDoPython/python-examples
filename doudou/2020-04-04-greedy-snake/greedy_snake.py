import pygame, sys, random
from pygame.locals import *

# 颜色配置
snake_color = pygame.Color("#8B7D1C")
food_color = pygame.Color("#8B0000")
background_color = pygame.Color("#BACB03")
text_color = pygame.Color("#EFEFEF")

speed = 5
# 长度单位
pixel = 15
line = 44
row = 36
window_width = pixel * line
window_high = pixel * row

point_left_up = [pixel * 2, pixel * 4]
point_left_down = [pixel * 2, pixel * (row - 2)]
point_right_up = [pixel * (line - 2), pixel * 4]
point_right_down = [pixel * (line - 2), pixel * (row - 2)]

# 蛇头位置
snake_head = [pixel * 8, pixel * 8]
# 蛇身
snake_body = [[snake_head[0] - x * pixel, snake_head[1]] for x in range(5)]
# 方向
direction_right = 0
direction_up = 90
direction_left = 180
direction_down = 270
move = {direction_right: [pixel, 0], direction_left: [-pixel, 0],
        direction_up: [0, -pixel], direction_down: [0, pixel]}

# 分数设置
score = 5
filename = 'db.txt'


def write_score(content):
    with open(filename, 'w+') as f:
        f.write(str(content))


def read_score():
    with open(filename, 'w+') as f:
        result = f.readline()
        return 0 if result.strip() == '' else int(result)


def init():
    # 初始化
    pygame.init()
    # new a window
    my_screen = pygame.display.set_mode((window_width, window_high), 0, 32)
    # 设置标题
    pygame.display.set_caption("Greedy Snake")
    return my_screen


# 游戏结束
def game_over(max_score, current_score):
    if max_score < current_score:
        write_score(current_score)
    pygame.quit()
    sys.exit()


screen = init()
time_clock = pygame.time.Clock()


# 画边线
def draw_box():
    for point in [[point_left_up, point_right_up], [point_right_up, point_right_down],
                  [point_right_down, point_left_down], [point_left_down, point_left_up]]:
        pygame.draw.line(screen, snake_color, point[0], point[1], 1)


def is_alive():
    # 越界 -> game over
    if (snake_head[0] < point_left_up[0] or snake_head[0] > (point_right_down[0] - pixel) or
            snake_head[1] < point_left_up[1] or snake_head[1] > (point_right_down[1]) - pixel):
        return False

    # 头触碰到身体 -> game over
    if snake_head in snake_body:
        return False

    return True


# 随机产生食物
def create_food():
    while True:
        x = random.randint(point_left_up[0] / pixel, point_right_down[0] / pixel - 1) * pixel
        y = random.randint(point_left_up[1] / pixel, point_right_down[1] / pixel - 1) * pixel
        if [x, y] not in snake_body:
            break
    return [x, y]


def draw_snake(food_position):
    # 画蛇
    for point in snake_body:
        pygame.draw.rect(screen, snake_color, Rect(point[0], point[1], pixel, pixel))
    # 画食物
    pygame.draw.rect(screen, food_color, Rect(food_position[0], food_position[1], pixel, pixel))


def display_message(text, color, size, postion):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, postion)
    pygame.display.update()


# 入口函数
def run():
    food_position = create_food()
    max_score = read_score()
    current_score = 0
    is_dead = False
    origin_direction = direction_right
    target_direction = origin_direction
    while True:
        # 监听键盘按键 退出 OR 换方向
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(max_score, current_score)
            if event.type == KEYDOWN:
                # 方向键 or asdw 控制方向
                if event.key == K_RIGHT or event.key == K_d:
                    target_direction = direction_right
                if event.key == K_LEFT or event.key == K_a:
                    target_direction = direction_left
                if event.key == K_UP or event.key == K_w:
                    target_direction = direction_up
                if event.key == K_DOWN or event.key == K_s:
                    target_direction = direction_down
                # esc 退出
                if event.key == K_ESCAPE:
                    game_over(max_score, current_score)
            # 夹角为 90 or 270 可以转换方向
            angle = abs(origin_direction - target_direction)
            if angle == 90 or angle == 270:
                origin_direction = target_direction

        if not is_dead:
            snake_head[0] += move[origin_direction][0]
            snake_head[1] += move[origin_direction][1]

        if not is_dead and is_alive():
            # 按 origin_direction 方向运动
            snake_body.insert(0, list(snake_head))
            # 吃到食物后重新生成
            if snake_head[0] == food_position[0] and snake_head[1] == food_position[1]:
                food_position = create_food()
                current_score += score
            else:
                # 移除最后一格
                snake_body.pop()
        else:
            is_dead = True

        # 画背景
        screen.fill(background_color)
        # 画边框
        draw_box()
        # 画蛇
        draw_snake(food_position)
        # 刷新画面
        pygame.display.update()
        # 更新分数
        display_message(f"{current_score}/{max_score}", text_color, 30, (pixel * 2, pixel * 2))
        if is_dead:
            display_message(f"Game Over", text_color, 50, (pixel * 16, pixel * 15))
        # 控制游戏速度
        time_clock.tick(speed)


if __name__ == '__main__':
    run()