import pygame

from pygame.locals import *
from random import randint
from gameobjects.vector2 import Vector2


class Star(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed


def run():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    stars = []

    for n in xrange(200):
        xx = float(randint(-10, 10))
        yy = float(randint(-10, 10))
        x = 320 + xx
        y = 240 + yy
        speed = Vector2(xx, yy)
        stars.append(Star(x, y, speed))

    clock = pygame.time.Clock()

    white = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if QUIT == event.type:
                return
            if KEYDOWN == event.type:
                return

        xx = float(randint(-10, 10))
        yy = float(randint(-10, 10))
        x = 320 + xx
        y = 240 + yy
        speed = Vector2(xx, yy)
        star = Star(x, y, speed)
        stars.append(star)

        time_passed = clock.tick()
        time_passed_second = time_passed / 1000.
        screen.fill((0, 0, 0))

        for star in stars:
            new_x = Vector2(0, 0)
            new_x.x = star.x + time_passed_second * star.speed.x
            new_x.y = star.y + time_passed_second * star.speed.y
            star.speed += time_passed_second*star.speed
            pygame.draw.aaline(screen, white, (star.x, star.y), (new_x.x, new_x.y))
            star.x = new_x.x
            star.y = new_x.y

        def on_screen(star):
            return 480 > star.y > 0 and 0 < star.x < 640

        stars = filter(on_screen, stars)
        pygame.display.update()


if __name__ == "__main__":
    run()
