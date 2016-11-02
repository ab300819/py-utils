#!-*-encoding:utf-8-*-
from multiprocessing.managers import BaseManager
from multiprocessing import Queue, Process


class Worker(Process):
    def __init__(self, q):
        self.q = q
        super(Worker, self).__init__()

    def run(self):
        for i in range(10):
            self.q.put(i)


class QueueManager(BaseManager):
    pass


def init():
    queue = Queue()

    w = Worker(queue)
    w.start()

    QueueManager.register('get_queue', callable=lambda: queue)
    m = QueueManager(address=('', 5000), authkey=b'abc')
    s = m.get_server()
    s.serve_forever()


if __name__ == '__main__':
    init()
