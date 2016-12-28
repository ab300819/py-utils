#!/usr/bin/env python3

import os
import time, random
from multiprocessing import Process, Pool


def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


def long_time_task(name):
    print('Run task %s(%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def create_single():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Children process will start.')
    p.start()
    p.join()
    print('Children process end.')


def create_multi():
    print('Parent process %s.' % os.getpgid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all suppresses done...')
    p.close()
    p.join()
    print('All subprocess done.')


if __name__ == '__main__':
    create_single()
