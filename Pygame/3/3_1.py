backname= "../11.png"

import pygame
from pygame.locals import *
from sys import exit

SCREENSIZE = (640, 480)


pygame.init()

screen = pygame.display.set_mode(SCREENSIZE, RESIZABLE, 32)
background = pygame.image.load(backname).convert()

while True:
    event = pygame.event.wait()
    if QUIT == event.type:
        exit()
    if VIDEORESIZE == event.type:
        SCREENSIZE=event.size
        print SCREENSIZE
        screen = pygame.display.set_mode(SCREENSIZE, RESIZABLE, 32)
        pygame.display.set_caption("window resize to "+str(event.size))

    screen_width, screen_height = SCREENSIZE
    for y in range(0, screen_width, background.get_height()):
        for x in range(0, screen_height, background.get_width()):
            screen.blit(background, (x,y))
    pygame.display.update()
        
    
