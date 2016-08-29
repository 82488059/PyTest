import pygame
from pygame.locals import *
from random import randint

pygame.init()
SCREEN_SIZE = (640, 480)
main_screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
# key down
ROTATE_LEFT, ROTATE_RIGHT, TO_BOTTOM = range(3)
# diamond size
DIAMOND_SIZE = (20, 20)
# color type
diamond_color_size = 6
COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_BLACK, COLOR_NO_DIAMOND = range(
    diamond_color_size)
COLOR = {
    COLOR_RED: (255, 0, 0),
    COLOR_BLUE: (0, 0, 255),
    COLOR_GREEN: (0, 255, 0),
    COLOR_YELLOW: (255, 255, 0),
    COLOR_BLACK: (0, 0, 0),
    COLOR_NO_DIAMOND: (100, 100, 100),
}

COLOR_DIAMOND = {
    COLOR_RED: pygame.surface.Surface(DIAMOND_SIZE).convert(),
    COLOR_BLUE: pygame.surface.Surface(DIAMOND_SIZE).convert(),
    COLOR_GREEN: pygame.surface.Surface(DIAMOND_SIZE).convert(),
    COLOR_YELLOW: pygame.surface.Surface(DIAMOND_SIZE).convert(),
    COLOR_BLACK: pygame.surface.Surface(DIAMOND_SIZE).convert(),
    COLOR_NO_DIAMOND: pygame.surface.Surface(DIAMOND_SIZE).convert(),
}


#
def draw_rect(lw, surface, rgb_color):
    rect = (lw, lw, DIAMOND_SIZE[0] - 2 * lw, DIAMOND_SIZE[1] - 2 * lw)
    pygame.draw.line(surface, rgb_color, (rect[0], rect[1]), (rect[0], rect[3]), lw)
    pygame.draw.line(surface, rgb_color, (rect[0], rect[1]), (rect[2], rect[1]), lw)
    pygame.draw.line(surface, rgb_color, (rect[0], rect[3]), (rect[2], rect[3]), lw)
    pygame.draw.line(surface, rgb_color, (rect[2], rect[1]), (rect[2], rect[3]), lw)
    return


for x in xrange(diamond_color_size):
    COLOR_DIAMOND[x].fill(COLOR[x])
    draw_rect(2, COLOR_DIAMOND[x], (128, 128, 128))

# begin time
clock = pygame.time.Clock()
# GAME SCREEN SIZE
GAME_SCREEN_SIZE = (10, 20)
GAME_SCREEN_MID = GAME_SCREEN_SIZE[0] / 2
# font
use_font = pygame.font.Font("FONT.TTF", 16)
# POINT
SCORE_POINT = (250, 100)
NEXT_DIAMOND_POINT = (12, 5)
MOVING_DIAMOND_OUT_POINT = (GAME_SCREEN_MID, 0)
SCREEN_MID_POINT = (GAME_SCREEN_SIZE[0]*DIAMOND_SIZE[0]/2, GAME_SCREEN_SIZE[1]*DIAMOND_SIZE[1]/2)


class World(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.game_surface = use_font.render("game over. enter any key to restart.", True
                                            , COLOR[COLOR_RED], COLOR[COLOR_BLUE])

        self.width = width
        self.height = height
        self.background = pygame.surface.Surface(
            (self.width * DIAMOND_SIZE[0] + 1, self.height * DIAMOND_SIZE[1] + 1)).convert()
        self.background.fill((200, 255, 200))
        self.no_diamond = COLOR_DIAMOND[COLOR_NO_DIAMOND]

        self.diamonds = {}
        self.diamond_id = 0
        self.init_diamonds()
        self.moving_diamond = self.create_diamond()
        self.moving_diamond.move_x(GAME_SCREEN_SIZE[0] / 2)
        self.next_diamond = self.create_diamond()
        self.next_diamond.move_x(NEXT_DIAMOND_POINT[0])
        self.game_over = False
        self.d_time = 0.
        self.score = 0
        self.score_surface = use_font.render("score: 0", True, COLOR[COLOR_BLACK], COLOR[COLOR_BLUE])
        return

    def init_value(self):
        self.diamonds = {}
        self.diamond_id = 0
        self.init_diamonds()
        self.moving_diamond = self.create_diamond()
        self.moving_diamond.move_x(GAME_SCREEN_SIZE[0] / 2)
        self.next_diamond = self.create_diamond()
        self.next_diamond.move_x(NEXT_DIAMOND_POINT[0])
        self.d_time = 0.
        self.score = 0
        self.score_surface = use_font.render("score: 0", True, COLOR[COLOR_BLACK], COLOR[COLOR_BLUE])
        self.game_over = False
        return

    def init_diamonds(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                self.diamonds[x, y] = None
        return

    def create_diamond(self):
        return Diamond(self)

    def process(self, process_time):
        if self.game_over:
            return
        self.d_time += process_time
        if self.d_time > 500.:
            self.d_time -= 500.
            if self.moving_diamond is None:
                self.moving_diamond = self.next_diamond
                self.moving_diamond.move_x(-NEXT_DIAMOND_POINT[0] + GAME_SCREEN_SIZE[0] / 2)
                self.next_diamond = self.create_diamond()
                self.next_diamond.move_x(NEXT_DIAMOND_POINT[0])
                return
            self.diamond_down()
        return

    def add_diamond_world(self, diamond):
        nodes = diamond.get_all_node()
        for k in nodes.keys():
            if nodes[k] is not None:
                self.diamonds[nodes[k].get_pos()] = nodes[k]
        self.moving_diamond = None
        self.erase()
        self.check_game()
        return

    def check_game(self):
        for x in xrange(0, self.width):
            if self.diamonds[x, 1] is not None:
                self.game_over = True
                return False
        return True

    def render_background(self, surface):
        surface.blit(self.background, (self.x, self.y))
        for x in xrange(self.width):
            for y in xrange(self.height):
                surface.blit(self.no_diamond, (self.x + x * DIAMOND_SIZE[0], self.y + y * DIAMOND_SIZE[1]))
        return

    def render(self, surface):
        self.render_background(surface)

        for diamond in self.diamonds.itervalues():
            if diamond is not None:
                diamond.render(surface)

        if self.moving_diamond:
            self.moving_diamond.render(surface)
        self.next_diamond.render(surface)

        surface.blit(self.score_surface, SCORE_POINT)
        if self.game_over:
            surface.blit(self.game_surface
                         , (SCREEN_MID_POINT[0]-self.game_surface.get_width()/2+self.x
                            , SCREEN_MID_POINT[1]-self.game_surface.get_height()/2+self.y))
        return

    def event_key_down(self, key):
        if self.game_over:
            self.init_value()
            return
        if K_LEFT == key:
            self.diamond_left()
        elif K_RIGHT == key:
            self.diamond_right()
        elif K_DOWN == key:
            self.diamond_down()
        elif K_UP == key:
            self.moving_diamond_rotate()
        return

    def moving_diamond_bottom(self):
        if self.moving_diamond is None:
            return
        self.moving_diamond.get_bottom()
        return

    def moving_diamond_rotate(self):
        if self.moving_diamond is None:
            return
        index = self.moving_diamond.get_next_rotate()
        for v in index.itervalues():
            if v[0] < 0 or v[0] >= self.width or v[1] >= self.height or self.diamonds[v] is not None:
                return
        self.moving_diamond.rotate()
        return

    def diamond_down(self):
        if self.moving_diamond is None:
            return
        bottom = self.moving_diamond.get_bottom()
        for i in bottom:
            next_pos = (bottom[i][0], bottom[i][1] + 1)
            if next_pos[1] >= self.height:
                self.add_diamond_world(self.moving_diamond)
                return
            if self.diamonds[next_pos] is not None:
                self.add_diamond_world(self.moving_diamond)
                return
        self.moving_diamond.move_y(1)
        return

    def diamond_left(self):
        if self.moving_diamond is None:
            return
        left = self.moving_diamond.get_left()
        for i in left:
            next_pos = (left[i][0] - 1, left[i][1])
            if next_pos[0] < 0 or self.diamonds[next_pos] is not None or self.width < next_pos[0]:
                return

        self.moving_diamond.move_x(-1)
        return

    def diamond_right(self):
        if self.moving_diamond is None:
            return
        left = self.moving_diamond.get_right()
        for i in left:
            next_pos = (left[i][0] + 1, left[i][1])
            if self.width <= next_pos[0] or self.diamonds[next_pos] is not None or next_pos[0] < 0:
                return
        self.moving_diamond.move_x(1)
        return

    def point_to_index(self, point):
        return (point[0] - self.x) / DIAMOND_SIZE[0], (point[1] - self.y) / DIAMOND_SIZE[1]

    def index_to_point(self, index):
        return index[0] * DIAMOND_SIZE[0] + self.x, index[1] * DIAMOND_SIZE[1] + self.y

    def erase(self):
        n = 0
        for line in xrange(0, self.height):
            if self.is_full(line):
                self.clear_line(line)
                n += 1
                self.drop_more_than_line(line)
                line -= 1
        self.score += n * n
        str = "score: %d" % self.score
        self.score_surface = use_font.render(str, True, COLOR[COLOR_BLACK], COLOR[COLOR_BLUE])
        return

    def drop_more_than_line(self, line):
        for y in xrange(0, line):
            for x in xrange(0, self.width):
                yy = line - y
                if self.diamonds[x, yy] is not None:
                    self.diamonds[x, yy].move_y(1)
                    self.diamonds[x, yy + 1] = self.diamonds[x, yy]
                    self.diamonds[x, yy] = None
        return

    def is_full(self, y):
        for x in xrange(0, self.width):
            if self.diamonds[x, y] is None:
                return False
        return True

    def clear_line(self, y):
        for x in xrange(0, self.width):
            self.diamonds[x, y] = None
        return


class Node(object):
    def __init__(self, x, y, background, world):
        self.x = x
        self.y = y
        self.background = background
        self.world = world
        return

    def render(self, surface):
        surface.blit(self.background, (self.world.index_to_point((self.x, self.y))))
        return

    def move_x(self, x):
        self.x += x
        return

    def move_y(self, y):
        self.y += y
        return

    def get_pos(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_pos(self, index):
        self.x = index[0]
        self.y = index[1]
        return


diamond_point_type_size = 7
diamond_point = {
    0: {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)},
    1: {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (0, 1)},
    2: {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (1, 1)},
    3: {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3)},
    4: {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (2, 1)},
    5: {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (2, 1)},
    6: {0: (1, 0), 1: (2, 0), 2: (0, 1), 3: (1, 1)},
}

diamond_rotate_point = {
    0: {0: {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)},  #
        1: {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)},
        2: {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)},
        3: {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)},
        },
    1: {0: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (0, 2)},  # L
        1: {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (1, 2)},
        2: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (2, 0)},
        3: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (2, 2)},
        },
    2: {0: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (1, 0)},  # T
        1: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (2, 1)},
        2: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (1, 2)},
        3: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (0, 1)},
        },
    3: {0: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (1, 3)},  # |
        1: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (3, 1)},
        2: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (1, 3)},
        3: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (3, 1)},
        },
    4: {0: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (2, 0)},  # !L
        1: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (2, 2)},
        2: {0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (0, 2)},
        3: {0: (0, 1), 1: (1, 1), 2: (2, 1), 3: (0, 0)},
        },
    5: {0: {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (2, 1)},  # Z
        1: {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 2)},
        2: {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (2, 1)},
        3: {0: (1, 0), 1: (1, 1), 2: (0, 1), 3: (0, 2)},
        },
    6: {0: {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (2, 0)},  # !Z
        1: {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 2)},
        2: {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (2, 0)},
        3: {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 2)},
        },
}


class Diamond(object):
    def __init__(self, world):
        self.x = 0
        self.y = 0
        self.diamonds = {}
        self.diamonds_list = {}
        self.diamond_id = 0
        self.init_diamonds()
        self.world = world
        self.type = None
        self.create(world)
        self.rotate_time = 0
        return

    def init_diamonds(self):
        for x in xrange(0, 4):
            for y in xrange(0, 4):
                self.diamonds[x, y] = None
        return

    def create(self, world):
        self.type = randint(0, diamond_point_type_size - 1)
        rand_color = randint(0, 3)
        index = diamond_rotate_point[self.type][0]
        self.diamonds_list[0] = self.diamonds[index[0][0], index[0][1]] = Node(index[0][0], index[0][1],
                                                                               COLOR_DIAMOND[rand_color], world)
        self.diamonds_list[1] = self.diamonds[index[1][0], index[1][1]] = Node(index[1][0], index[1][1],
                                                                               COLOR_DIAMOND[rand_color], world)
        self.diamonds_list[2] = self.diamonds[index[2][0], index[2][1]] = Node(index[2][0], index[2][1],
                                                                               COLOR_DIAMOND[rand_color], world)
        self.diamonds_list[3] = self.diamonds[index[3][0], index[3][1]] = Node(index[3][0], index[3][1],
                                                                               COLOR_DIAMOND[rand_color], world)
        self.diamond_id = 4
        return

    def turn(self):
        if self.type == 0:
            return
        return

    def render(self, surface):
        for diamond in self.diamonds.itervalues():
            if diamond is not None:
                diamond.render(surface)
        return

    def move_x(self, x):
        for diamond in self.diamonds.itervalues():
            if diamond is not None:
                diamond.move_x(x)
        self.x += x
        return

    def move_to(self, pos):
        x = self.x - pos[0]
        y = self.y - pos[1]
        for diamond in self.diamonds.itervalues():
            if diamond is not None:
                diamond.move_x(x)
                diamond.move_x(x)
        return

    def move_y(self, y):
        for diamond in self.diamonds.itervalues():
            if diamond is not None:
                diamond.move_y(y)
        self.y += y
        return

    def get_left(self):
        left = {}
        for y in xrange(0, 4):
            for x in xrange(0, 4):
                if self.diamonds[3 - x, y] is not None:
                    left[y] = self.diamonds[3 - x, y].get_pos()
        return left

    def get_right(self):
        right = {}
        for y in xrange(0, 4):
            for x in xrange(0, 4):
                if self.diamonds[x, y] is not None:
                    right[y] = self.diamonds[x, y].get_pos()
        return right

    def get_bottom(self):
        bottom = {}
        for x in xrange(0, 4):
            for y in xrange(0, 4):
                if self.diamonds[x, y] is not None:
                    bottom[x] = self.diamonds[x, y].get_pos()
        return bottom

    def get_all_node(self):
        return self.diamonds

    def get_next_rotate(self):
        c_index = diamond_rotate_point[self.type][(self.rotate_time + 1) % 4].copy()
        for k in c_index.keys():
            c_index[k] = (self.x + c_index[k][0], self.y + c_index[k][1])
        return c_index

    def rotate(self):
        self.rotate_time = (self.rotate_time + 1) % 4
        n = 0
        for x in xrange(0, 4):
            for y in xrange(0, 4):
                self.diamonds[x, y] = None
        for i in xrange(0, 4):
            new_pos = diamond_rotate_point[self.type][self.rotate_time][i]
            new_pos_now = (new_pos[0] + self.x, new_pos[1] + self.y)
            self.diamonds_list[i].set_pos(new_pos_now)
            self.diamonds[new_pos] = self.diamonds_list[i]
        return


class App(object):
    def __init__(self):
        self.screen = main_screen
        # background init
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        # World init
        self.world = World(10, 10, GAME_SCREEN_SIZE[0], GAME_SCREEN_SIZE[1])
        self.create_world()
        return

    def create_world(self):
        self.world = World(10, 10, GAME_SCREEN_SIZE[0], GAME_SCREEN_SIZE[1])
        return

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.world.event_key_down(event.key)

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.world.event_key_down(K_LEFT)
            if pressed_keys[K_RIGHT]:
                self.world.event_key_down(K_RIGHT)
            if pressed_keys[K_DOWN]:
                self.world.event_key_down(K_DOWN)

            self.render()
            time_passed = clock.tick(30)
            self.world.process(time_passed)
            self.world.render(self.screen)

            pygame.display.update()
        return

    def render(self):
        self.screen.blit(self.background, (0, 0))
        return


if __name__ == "__main__":
    app = App()
    app.run()
