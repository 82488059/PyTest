#!/usr/bin/env python
import wx


class Study(object):
    def __init__(self):

        return

class Live(object):
    def __init__(self):
        return


class Work(object):
    def __init__(self):
        return

    def ZaiJiaXiuXi(self, o):
        o.PiLao -= 20
        if o.PiLao < 0:
            o.PiLao = 0
        return



class Child(object):
    def __init__(self):
        self.ZhiLi = 0
        self.NeiLi = 0
        self.NaiLi = 0
        self.QiZhi = 0
        self.MingQi = 0
        self.WanXing = 0
        self.DaoDe = 0
        self.PanNi = 0
        self.age = 0
        self.tired = 0





app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()





