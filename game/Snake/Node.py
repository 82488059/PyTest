from GameSnake import *
from gameobjects.vector2 import Vector2


class Node(object):
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        # self.destination = Vector2(0, 0)
        self.id = 0

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))

    def set_location(self, location):
        self.location.x = location.x
        self.location.y = location.y

    def get_location(self):
        return self.location

    def move(self, destination):
        if 0 < self.location.x < SCREEN_SIZE[0] and 0 < self.location < SCREEN_SIZE[1]:
            self.location += destination
        else:
            self.location += destination
            self.location.x %= SCREEN_SIZE[0]
            self.location.y %= SCREEN_SIZE[1]

    def process(self, time_passed):
        self
        return

    def near(self, pos):
        t = self.location - pos
        if -5 < t.x < 5 and -5 < t.y < 5:
            return True
        return False
