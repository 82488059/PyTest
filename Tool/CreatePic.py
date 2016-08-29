import pygame
from pygame.locals import *

pygame.init()
string = "EXIT GAME"
FONT = pygame.font.Font("FONT.TTF", 24)
png = FONT.render(string, True, (255, 255, 255), (0, 0, 0))
pygame.image.save(png, string+".bmp")
