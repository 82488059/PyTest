SCREEN_SIZE = (640, 480)
NODE_SIZE = 10

NODE_LEFT = (-10, 0)
NODE_RIGHT = (10, 0)
NODE_UP = (0, -10.)
NODE_DOWN = (0, 10)

import pygame

from World import *
from random import randint
from pygame.locals import *
from Snake import *
from Node import *
from sys import exit


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
food_image = pygame.surface.Surface((NODE_SIZE, NODE_SIZE)).convert()
food_image.fill((100, 255, 100))


class App(object):
    def __init__(self):
        # pygame.init()
        self.screen = screen
        self.node_image = pygame.surface.Surface((NODE_SIZE, NODE_SIZE)).convert()
        self.world = World(self, SCREEN_SIZE)
        self.snake = Snake(self.world, "snake")

        return

    def product_food(self):
        node = Node(self.world, "head", food_image)
        x = randint(0, 64)
        y = randint(0, 48)
        node.set_location(Vector2(x*10, y*10))
        self.world.add_food(node)
        return

    def create_food(self):
        food = Node(self.world, "head", food_image)
        return food

    def run(self):
        clock = pygame.time.Clock()
        node1 = Node(self.world, "head", self.node_image)
        node1.set_location(Vector2(Vector2(20, 0)))
        self.snake.add_node(node1)
        node2 = Node(self.world, "body", self.node_image)
        node2.set_location(Vector2(10, 0))
        self.snake.add_node(node2)
        self.world.add_snake(self.snake)
        self.product_food()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if K_LEFT == event.key:
                        self.snake.set_turn(Vector2(NODE_LEFT))
                    elif K_RIGHT == event.key:
                        self.snake.set_turn(Vector2(NODE_RIGHT))
                    elif K_DOWN == event.key:
                        self.snake.set_turn(Vector2(NODE_DOWN))
                    elif K_UP == event.key:
                        self.snake.set_turn(Vector2(NODE_UP))

            time_passed = clock.tick(30)

            self.world.process(time_passed)
            self.world.render(self.screen)

            pygame.display.update()

if __name__ == "__main__":
    app = App()
    app.run()


