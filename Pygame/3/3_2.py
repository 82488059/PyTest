bkimagename = '../11.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
back = pygame.image.load(bkimagename).convert()
fullscreen = False
while True:
    for event in pygame.event.get():
        if QUIT == event.type:
            exit()
    if KEYDOWN == event.type:
        if K_f == event.key:
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
            else:
                screen = pygame.display.set_mode((640, 480), 0, 32)
    screen.blit(back, (0, 0))
    pygame.display.update()
