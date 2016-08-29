from GameSnake import *
from gameobjects.vector2 import Vector2


class Snake(object):
    def __init__(self, world, name):
        self.world = world
        self.name = name
        self.destination = Vector2(NODE_RIGHT)
        self.turn = Vector2(NODE_RIGHT)
        self.node_id = 0
        self.nodes = {}
        self.left_time = 0.
        return

    def add_node(self, node):
        self.nodes[self.node_id] = node
        node.id = self.node_id
        self.node_id += 1
        return

    def render(self, surface):
        for node in self.nodes.values():
            node.render(surface)
        return

    def check_destination(self):
        if self.turn != -1*self.destination:
            self.destination.x = self.turn.x
            self.destination.y = self.turn.y
        return

    def process(self, time_passed):
        self.left_time += time_passed
        if self.left_time > 0.1 and self.node_id > 0:
            self.left_time = 0.
            self.check_destination()
            self.eat()
            self.move_body()
            self.move_head()
        return

    def eat(self):
        food = self.world.take_food(self.get_next_pos())
        if food:
            self.add_node(food)
        return

    def get_next_pos(self):
        next_pos = self.nodes[0].location + self.destination
        if not (0 < next_pos.x < SCREEN_SIZE[0] and 0 < next_pos < SCREEN_SIZE[1]):
            next_pos.x %= SCREEN_SIZE[0]
            next_pos.y %= SCREEN_SIZE[1]
        return next_pos

    def move_head(self):
        self.nodes[0].move(self.destination)
        return

    def move_body(self):
        if self.node_id < 2:
            return

        for i in xrange(1, self.node_id):
            t = self.node_id - i
            self.nodes[t].set_location(self.nodes[t-1].get_location())
        return

    def set_turn(self, des):
        # if des != -1*self.turn:
        self.turn.x = des.x
        self.turn.y = des.y
        return


