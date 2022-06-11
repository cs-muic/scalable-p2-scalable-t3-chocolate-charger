import os 
import redis
from rq import Worker, Queue, Connection
from redisConnection import extract_queue, redis_conn



if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(extract_queue, connection=redis_conn)
        worker.work()

