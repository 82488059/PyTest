#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


class TaskBase(object):
    def __init__(self, func, *args, **kwargs):
        """task base"""
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self, value):
        """task run_with_multi_thread"""
        ret = self.func(value, *self.args, **self.kwargs)
        return ret

