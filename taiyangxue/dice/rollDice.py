import random
import sys
import time

import pygame


class Dice:
    def __init__(self):
        self.diceRect = pygame.Rect(200, 225, 100, 100)
        self.diceSpin = [
            pygame.image.load("asset/rolling/4.png"),
            pygame.image.load("asset/rolling/3.png"),
            pygame.image.load("asset/rolling/2.png"),
            pygame.image.load("asset/rolling/1.png")
        ]
        self.diceStop = [
            pygame.image.load("asset/dice/1.png"),
            pygame.image.load("asset/dice/2.png"),
            pygame.image.load("asset/dice/3.png"),
            pygame.image.load("asset/dice/4.png"),
            pygame.image.load("asset/dice/5.png"),
            pygame.image.load("asset/dice/6.png")
        ]

        self.StopStatus = random.randint(0, 5)
        self.SpinStatus = 0

    def move(self):
        self.SpinStatus += 1
        if self.SpinStatus == len(self.diceSpin):
            self.SpinStatus = 0

class Game:
    def __init__(self, width=500, height=600):
        pygame.init()
        size = width, height
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

        self.rollTimes = 0  # 掷骰子过程的帧数记录
        self.Dice = Dice()
        self.start = False  # 状态标识
        self.rollCount = random.randint(3, 10)  # 初始投掷帧数

    def roll(self):
        self.screen.blit(self.Dice.diceSpin[self.Dice.SpinStatus], self.Dice.diceRect)
        self.Dice.move()
        self.rollTimes += 1
        if self.rollTimes > self.rollCount:
            self.start = False
            self.rollCount = random.randint(3, 10)
            self.Dice.StopStatus = random.randint(0, 5)
            self.rollTimes = 0

    def stop(self):
        self.screen.blit(self.Dice.diceStop[self.Dice.StopStatus], self.Dice.diceRect)

    def run(self):
        while True:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if ((event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE) \
                or event.type == pygame.MOUSEBUTTONDOWN) \
                and self.start == False:
                    self.start = True

            if self.start:
                self.roll()
            else:
                self.stop()
            pygame.display.update()
        

if __name__ == '__main__':
    Game().run()
