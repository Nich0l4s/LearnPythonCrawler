#!/usr/bin/env python
# encoding=utf-8

import os
import LaGou
import queue
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

m = QueueManager(address=('127.0.0.1', 50000), authkey=b'crawler')
m.connect()

task = m.get_task_queue()
result = m.get_result_queue()
if not os.path.exists(LaGou.LOGO_PATH):
    os.mkdir(LaGou.LOGO_PATH)
while True:
    try:
        data = task.get(timeout=10)
        LaGou.get_info(data)
        result.put(data['pn'])
    except queue.Empty:
        print('worker exit')

