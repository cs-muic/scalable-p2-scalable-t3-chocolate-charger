import os

import redis
from rq import Queue

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis://redis"),
    port=os.getenv("REDIS_PORT", "6379"),
    password=os.getenv("REDIS_PASSWORD", ""),
)

extract_queue = Queue('Extraction', connection=redis_conn)
compose_queue = Queue('Composer', connection=redis_conn)
log_queue = Queue('Log', connection=redis_conn)