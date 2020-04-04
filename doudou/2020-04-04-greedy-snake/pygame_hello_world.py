import pygame, sys

# init
pygame.init()
# new a window
screen = pygame.display.set_mode((640, 480))
# title
pygame.display.set_caption("Hello World")
font = pygame.font.Font(None, 30)
text = font.render('Hello World', True, pygame.Color("#FFFFFF"))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(text, (100, 100))
    pygame.display.update()
