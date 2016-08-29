# -*- coding: cp936 -*-
name = "eqeq"
pngname = 'name.png'
import pygame
from pygame.locals import *
from sys import exit


pygame.init()
font = pygame.font.SysFont("微软雅黑", 64)
namesurface = font.render(name, True, (0,0,0), (255,255,255))
pygame.image.save(namesurface, "name.png")

screen = pygame.display.set_mode((640, 480), 0, 32)
#fontimage = pygame.image.load(pngname).convert()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    fontimage = pygame.image.load(pngname).convert()
    screen.blit(fontimage, (0,0))
    pygame.display.update()
            
