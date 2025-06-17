'''
This module will listen to queued tasks and process them as they are received.
'''

import os
import redis
from rq import Worker, Queue
from redis import Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    # 创建每个队列并绑定到同一个 Redis 连接
    queues = [Queue(name, connection=conn) for name in listen]
    # 创建 Worker 实例，监听指定队列
    worker = Worker(queues, connection=conn)
    worker.work()

