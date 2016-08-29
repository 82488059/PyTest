import pygame
#from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

all_color = pygame.Surface((4096, 4096), depth=24)


for r in xrange(256):
    print r+1, "out of 256"
    x = (r&15)*255
    y = (r>>4)*255
    for g in xrange(256):
        for b in xrange(256):
            all_color.set_at((x+g, y+b), (r, g, b))
pygame.image.save(all_color, 'allcolor.bmp')
#back = pygame.image.load('allcolor.bmp').convert()
#screen.blit(back, (0,0))
#pygame.display.update()
