#!/usr/bin/env python
# encoding=utf-8

import queue
import LaGou
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

task_queue, result_queue = queue.Queue(), queue.Queue()


def task():
    return task_queue


def result():
    return result_queue


class QueueManager(BaseManager):
    pass


def server():
    QueueManager.register('get_task_queue', callable=task)
    QueueManager.register('get_result_queue', callable=result)

    manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'crawler')

    manager.start()

    task_q = manager.get_task_queue()
    result_q = manager.get_result_queue()

    total = LaGou.get_total_page(LaGou.DOWNLOAD_URL)
    for i in range(1, int(total) + 1):
        data = {
            'first': 'false',
            'pn': str(i),
            'kd': 'Python'
        }
        task_q.put(data)
    while result_q.qsize() < total:
        pass
    manager.shutdown()
if __name__ == '__main__':
    freeze_support()
    server()


