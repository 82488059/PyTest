#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import queue


class Pool(object):
    def __init__(self, create_func, size):
        self.init = False
        self.size = size
        self.create_func = create_func
        self.queue = queue.Queue()
        self.total = 0

    def put(self, obj):
        self.queue.put(obj)
        # print(self.queue.qsize())

    def get(self):
        if not self.init:
            self.init_pool()

        if self.queue.empty():
            self.total += 1
            print('pool total {}'.format(self.total))
            return self.create_func()
        return self.queue.get()

    def init_pool(self):
        if self.init:
            return True
        for x in range(0, self.size):
            obj = self.create_func()
            self.total += 1
            if obj:
                self.queue.put(obj)
            else:
                raise 0
        self.init = True
        return True

    def clear(self):
        self.queue = queue.Queue()
        self.init = False
        self.total = 0
