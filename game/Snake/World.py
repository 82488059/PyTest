from GameSnake import *
from random import randint
from gameobjects.vector2 import Vector2


class World(object):
    def __init__(self, game, background_size):
        self.size = (background_size[0], background_size[1])
        self.game = game
        self.snake = []
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.surface.Surface(self.size).convert()
        self.background.fill((255, 255, 255))

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def add_snake(self, snake):
        self.snake = snake
        return

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        self.snake.process(time_passed_seconds)
        for entity in self.entities.values():
            entity.process(time_passed_seconds)

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        self.snake.render(surface)
        for entity in self.entities.itervalues():
            entity.render(surface)

    def add_food(self, node):
        self.add_entity(node)
        return

    def take_food(self, pos):
        for entity in self.entities.itervalues():
            if entity.near(pos):
                self.remove_entity(entity)
                self.product_food()
                return entity
        return

    def no_food(self):
        for _ in self.entities.itervalues():
            return False
        return True

    def product_food(self):
        food = self.game.create_food()
        x = randint(0, 63)
        y = randint(0, 47)
        food.set_location(Vector2(x*10, y*10))
        self.add_food(food)
        return
