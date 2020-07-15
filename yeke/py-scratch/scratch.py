import os
import sys
import random
import pygame

path = 'prize'
ptype = ['jpg', 'png', 'bmp', 'JPG', 'PNG', 'BMP']
# 窗口大小
screen_size = (600, 400)
white = (255, 255, 255, 20)
gray = (192, 192, 192)
pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.diamond)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('刮一刮抽奖')
surface = pygame.Surface(screen_size).convert_alpha()
surface.fill(gray)
filenames = os.listdir(path)
filenames = [f for f in filenames if f.split('.')[-1] in ptype]
imgpath = os.path.join(path, random.choice(filenames))
image_used = pygame.transform.scale(pygame.image.load(imgpath), screen_size)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(-1)
	mouse_event = pygame.mouse.get_pressed()
	if mouse_event[0]:
		pygame.draw.circle(surface, white, pygame.mouse.get_pos(), 40)
	elif mouse_event[-1]:
		surface.fill(gray)
		image_used = pygame.transform.scale(pygame.image.load(imgpath), screen_size)
	screen.blit(image_used, (0, 0))
	screen.blit(surface, (0, 0))
	pygame.display.update()


