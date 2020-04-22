import random, pygame

FONT_PX = 15
pygame.init()
winSur = pygame.display.set_mode((400, 500))
font = pygame.font.SysFont('arial', 16)
bg_suface = pygame.Surface((400, 500), flags=pygame.SRCALPHA)
pygame.Surface.convert(bg_suface)
bg_suface.fill(pygame.Color(0, 0, 0, 13))
winSur.fill((0, 0, 0))
# 数字
texts = [font.render(str(i), True, (0, 255, 0)) for i in range(10)]
colums = int(400 / FONT_PX)
drops = [0 for i in range(colums)]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.time.delay(33)
    winSur.blit(bg_suface, (0, 0))
    for i in range(len(drops)):
        text = random.choice(texts)
        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))
        drops[i] += 1
        if drops[i] * 10 > 400 or random.random() > 0.95:
            drops[i] = 0
    pygame.display.flip()
