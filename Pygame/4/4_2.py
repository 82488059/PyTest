# -*- coding: utf-8 -*-
#
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

font = pygame.font.Font('../DejaVuSansMono.ttf', 40)

text = font.render(u"hello", True, (0, 0, 255))

x = 0
y = (480-text.get_height())/2

back = pygame.image.load("../11.png").convert()

while True:
    for event in pygame.event.get():
        if QUIT == event.type:
            exit()

    screen.blit(back, (0,0))

    x-=0.2
    if x < -text.get_width():
        x = 640-text.get_width()
    screen.blit(text, (x,y))
    pygame.display.update()
