#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


from multiprocessing import cpu_count
import threading
import time
import datetime


# queue is Queue and run_with_multi_thread task.run_with_multi_thread()
class TaskThread(threading.Thread):
    def __init__(self, task, queue):
        super(TaskThread, self).__init__()
        self.task = task
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            print(u'task queue size {}'.format(self.queue.qsize()-1))
            # 取
            value = self.queue.get(False)
            # if not value:
            #    break
            # 空
            if not self.task.run(value):
                # 放回
                self.queue.put(value)
        # DebugPrint(u'thread end')

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def run_with_multi_thread(task, queue, thread_size=2*cpu_count()):
    print(datetime.datetime.now())
    print(u'run_with_multi_thread begin')
    dt = time.time()
    print(u'线程数：{} 队列大小：{}'.format(thread_size, queue.qsize()))
    thread_list = []
    for x in range(0, thread_size):
        td = TaskThread(task, queue)
        thread_list.append(td)
        td.start()
        time.sleep(0.25)
    for x in thread_list:
        x.join()
    dt = time.time() - dt
    print(datetime.datetime.now())
    print(u'run_with_multi_thread end, take time is {} seconds!'.format(dt))
    return True
