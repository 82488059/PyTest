background_filename = '../11.png'
sprite_filename = '../2.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load(background_filename).convert()
sprite = pygame.image.load(sprite_filename)

clock = pygame.time.Clock()
speed = 250

x = 0

while True:
    for event in pygame.event.get():
        if QUIT == event.type:
            exit()
    screen.blit(background, (0, 0))
    screen.blit(sprite, (x, 100))

    time_passed = clock.tick()
    time_passed_second = time_passed / 1000.0

    distance_moved = time_passed_second*speed
    
    x += distance_moved

    if x > 640:
        x = 0.

    pygame.display.update()
