from multiprocessing import Pool
import os, time, random


def long_time_task(name):
    print('Run long task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f second.' % (name, (end - start)))


def short_time_task(name):
    print('Run short task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f second.' % (name, (end - start)))


if __name__ == '__main__':
    print('Parent process %s...' % os.getpid())
    p = Pool()
    a = Pool()
    for i in range(15):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocessses done...')
    p.close()
    p.join()
    print('long done!')
    for j in range(20):
        a.apply_async(short_time_task, args=(j,))
    a.close()
    a.join()
    print('short done!')
