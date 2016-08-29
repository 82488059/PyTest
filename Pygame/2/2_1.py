bkimage_filename = '../11.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE=(640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
background = pygame.image.load(bkimage_filename).convert()
x,y = 0,0
movex,movey=0,0

while True:
    for event in pygame.event.get():
        if QUIT == event.type:
            exit()
        if KEYDOWN == event.type:
            if K_LEFT == event.key :
                movex=-1
            elif K_RIGHT == event.key :
                movex=1
            elif K_UP == event.key :
                movey=-1
            elif K_DOWN == event.key :
                movey=1
        elif KEYUP == event.type:
            movex=0
            movey=0

    y+=movey
    x+=movex

    screen.fill((0,0,0))
    screen.blit(background, (x, y))
                    
    pygame.display.update()
    
    
