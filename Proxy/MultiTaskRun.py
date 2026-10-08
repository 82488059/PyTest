#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import MultiRun
import Task
from multiprocessing import cpu_count
import queue


def init_queue(thread_size):
    q = queue.Queue()
    for i in range(thread_size):
        q.put(i)
    return q


def multi_thread_run_base_task(q, func, thread_size=2*cpu_count(), *args, **kwargs):
    task = Task.TaskBase.TaskBase(func, *args, **kwargs)
    MultiRun.TaskThread.run_with_multi_thread(task, q, thread_size)
    return True
