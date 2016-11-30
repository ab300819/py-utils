#!-*-encoding:utf-8-*-

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue')
m = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
m.connect()
for i in range(10):
    queue = m.get_queue()
    print(queue.get())
