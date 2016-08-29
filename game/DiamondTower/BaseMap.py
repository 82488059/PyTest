import pygame


class BaseMap(object):
    def __init__(self, main):
        self.dTime = 0
        self.main = main
        return

    def GetMain(self):
        return self.main

    def Render(self, surface):
        return

    def Process(self, dTime):
        return

    def ButtonDown(self, event):
        return