import os 
import sys 
import redis
from rq import Worker, Queue, Connection
from redisConnection import *
from features import *



if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(extract_queue, connection=redis_conn)
        worker.work()

