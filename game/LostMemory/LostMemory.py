import pygame
from pygame.locals import *
from World import *


class LostMemoryApp(object):
    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        self.world = World(self.WIDTH, self.HEIGHT)

        return

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.world.event_key_down(K_LEFT)
            if pressed_keys[K_RIGHT]:
                self.world.event_key_down(K_RIGHT)
            if pressed_keys[K_DOWN]:
                self.world.event_key_down(K_DOWN)
            if pressed_keys[K_UP]:
                self.world.event_key_down(K_UP)

            time_passed = clock.tick(30)
            self.world.process(time_passed)
            self.world.render(self.screen)

            pygame.display.update()

        return


if __name__ == "__main__":
    app = LostMemoryApp()
    app.run()
