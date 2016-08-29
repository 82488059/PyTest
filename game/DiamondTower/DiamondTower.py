from pygame.locals import *

from Button import *
from BaseMap import *

pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_MAX = (SCREEN_WIDTH, SCREEN_HEIGHT)
MAIN_MENU_FONT = pygame.font.Font("FONT.TTF", 24)


class LeftBar(BaseMap):
    def __init__(self, main):
        self.main = main
        return


class GameMap(BaseMap):
    def __init__(self, main):
        self.main = main
        self.leftBar = LeftBar()
        return


class StartMenu(BaseMap):
    def __init__(self, main):
        self.main = main
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.startButton = Button("START GAME.png", (self.width/2, self.height/2-30))
        self.settingButton = Button("SETTING GAME.png", (self.width/2, self.height/2))
        self.exitButton = Button("EXIT GAME.png", (self.width/2, self.height/2+30))
        return

    def Render(self, surface):
        self.startButton.render(surface)
        self.settingButton.render(surface)
        self.exitButton.render(surface)
        return

    def ButtonDown(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.startButton.is_over(event.pos):
                self.main.Start()
            elif self.settingButton.is_over(event.pos):
                self.main.Setting()
            elif self.exitButton.is_over(event.pos):
                self.main.Exit()
        return


class App(object):
    def __init__(self):
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        # background init
        self.background = self.create_background()
        self.level = 1
        # World init
        self.curMap = StartMenu(self)
        return

    def create_background(self):
        diamond = pygame.image.load("ground.png").convert()
        background = pygame.surface.Surface((self.width, self.height)).convert()
        for vx in xrange(0, 16):
            for vy in xrange(0, 12):
                background.blit(diamond, (vx*40, vy*40))

        return background

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

                if event.type == MOUSEBUTTONDOWN:
                    self.curMap.ButtonDown(event)

            self.render()
            time_passed = clock.tick(30)
            self.curMap.Process(time_passed)
            self.curMap.Render(self.screen)

            pygame.display.update()
        return

    def render(self):
        self.screen.blit(self.background, (0, 0))
        return

    def Start(self):
#        self.curMap =
        return

    def Setting(self):
        return

    def Exit(self):
        self.level = 1
        exit()
        return

if __name__ == "__main__":
    app = App()
    app.run()
