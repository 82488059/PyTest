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

x, y = 100., 100.
speedx, speedy = 133., 170.

while True:
    for event in pygame.event.get():
        if QUIT == event.type:
            exit()
    screen.blit(background, (0, 0))
    screen.blit(sprite, (x, y))

    time_passed = clock.tick()
    time_passed_second = time_passed / 1000.0

    x += speedx*time_passed_second
    y += speedy*time_passed_second


    if x > 640 - sprite.get_width():
        speedx = -speedx
        x = 640 - sprite.get_width()
    elif x < 0:
        speedx = -speedx
        x = 0.

    if y > 480 - sprite.get_height():
        speedy = -speedy
        y = 480 - sprite.get_height()
    elif y < 0:
        speedy = -speedy
        y = 0

    pygame.display.update()

    pygame.display.update()
