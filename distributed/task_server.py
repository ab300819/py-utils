#!-*-encoding:utf-8-*_
from multiprocessing.managers import BaseManager
from multiprocessing import Queue, Process
import random


class Worker(Process):
    def __init__(self, task, result):
        self.task = task
        self.result = result
        super(Worker, self).__init__()

    def run(self):
        for i in range(10):
            n = random.randint(0, 10000)
            self.task.put(n)
            print('Put task %d...' % n)
        for j in range(10):
            r = self.result.get()
            print('Get result %s' % r)
        print('Done!')


class QueueManager(BaseManager):
    pass


def start_distributed():
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('', 5000), authkey=b'abc')
    task_queue = Queue()
    result_queue = Queue()
    w = Worker(task_queue, result_queue)
    w.start()
    s = manager.get_server()
    s.serve_forever()

if __name__ == '__main__':
    start_distributed()
