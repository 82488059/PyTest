# -*- coding:utf-8 -*-
from random import randint
import pygame
from pygame.locals import *

MAZE_MAX = 50
MOVE_RIGHT = (1, 0)
MOVE_LEFT = (-1, 0)
MOVE_UP = (0, -1)
MOVE_DOWN = (0, 1)
direction = {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}, 2: {0: 0, 1: -1}, 3: {0: -1, 1: 0}}


class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.isWalk = False
        self.parent = self
        self.cost = 1.0

        return


class App(object):
    def __init__(self):
        self.map1 = {}
        for x in xrange(0, MAZE_MAX + 2):
            self.map1[x] = {}
            for y in xrange(0, MAZE_MAX + 2):
                self.map1[x][y] = 0
        pygame.init()
        screen_size = (640, 480)
        diamonds_size = (10, 10)

        self.screen = pygame.display.set_mode(screen_size, 0, 32)
        self.background = pygame.surface.Surface(screen_size).convert()
        self.diamonds1 = pygame.surface.Surface(diamonds_size).convert()
        self.diamonds2 = pygame.surface.Surface(diamonds_size).convert()
        self.background.fill((255, 255, 255))
        self.diamonds1.fill((128, 128, 128))
        self.diamonds2.fill((0, 0, 0))
        self.x = 22
        self.y = 22
        return

    def make_maze(self, num):
        if num == 0:
            return

        x = randint(0, self.x*2)
        y = randint(0, self.y*2)
        d_index = randint(0, 3)
        length = randint(5, 20)

        for i in xrange(0, length):
            nx = x + direction[d_index][0]*i
            ny = y + direction[d_index][1]*i
            if 0 < nx < self.x*2+2 and 0 < ny < self.y*2+2:
                self.map1[nx][ny] = 0xffffffff
            else:
                break
        self.make_maze(num-1)
        return

    def run(self):
        self.x = 22
        self.y = 22
        self.make_maze(25)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            self.render()
        return

    def render(self):
        self.screen.blit(self.background, (0, 0))

        for z2 in xrange(1, self.y * 2 + 1 + 1):
            for z1 in xrange(1, self.x * 2 + 1 + 1):
                if self.map1[z1][z2] == 0:
                    self.screen.blit(self.diamonds1, (z1*10, z2*10))
                else:
                    self.screen.blit(self.diamonds2, (z1*10, z2*10))

        pygame.display.update()

        return

    def a_star(self):



        return




if __name__ == "__main__":
    app = App()
    app.run()
