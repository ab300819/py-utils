#!-*-encoding:utf-8-*-
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue')
m = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
m.connect()
queue = m.get_queue()
queue.put('hello')
