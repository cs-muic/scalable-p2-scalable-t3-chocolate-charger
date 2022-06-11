from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio
import subprocess
from redisConnection import redis_conn, extract_queue, compose_queue, log_queue


def frames_extraction(filename, workId): 
    # pull video from minio
    minio.download_video(filename)
    path = str.split(filename, '.')[0]
    print(path)
    # perfrom sh script
    process = subprocess.Popen(f'sh ./scripts/extract.sh ./temp/{filename} frames', shell=True, stdout=subprocess.PIPE)
    process.wait()
    # upload frames back to minio
    minio.upload_folder("./frames", workId)
    print(f"extraction {workId} done")
    # update state of the job
    job_worker3 = log_queue.enqueue(update__done_status, 1, workId)
    # push to queue 2
    job_worker2 = compose_queue.enqueue(image_compose, workId)