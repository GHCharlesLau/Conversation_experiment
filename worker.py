'''
This module will listen to queued tasks and process them as they are received.
'''
import os
import redis
from rq import Worker, Queue
import platform

listen = ['high', 'default', 'low']
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if platform.system() == "Windows":
    # Windows系统使用线程池
    from rq.worker import SimpleWorker as WorkerClass
    # Windows不支持SIGALRM，禁用超时或使用自定义实现
    timeout_param = None
else:
    # Linux/Mac使用默认进程池
    from rq.worker import Worker as WorkerClass
    # Linux/Mac使用正常超时设置
    timeout_param = 180  # 3分钟超时


if __name__ == '__main__':
    # 创建每个队列并绑定到同一个 Redis 连接
    queues = [Queue(name, connection=conn) for name in listen]
    # 创建 Worker 实例，监听指定队列
    worker = WorkerClass(queues, connection=conn)
    worker.work()

