from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio
import subprocess
from redisConnection import redis_conn, extract_queue, compose_queue, log_queue


######################### Below this line Using 3 queue (The thrid is Log queue) ################################

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
    job_worker3 = log_queue.enqueue(update__done_status, 1, workId, filename)
    # push to queue 2
    job_worker2 = compose_queue.enqueue(image_compose, workId, filename, job_timeout='1h')


def image_compose(workId, filename):
    # download all frames
    minio.download_extracted_frames(workId)
    # perfrom sh script
    process = subprocess.Popen(f'sh ./scripts/compose.sh ./download/{workId} {workId}.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(f"Done {workId}")
    # update state of the job and get url
    minio.upload_gif(f"./{workId}.gif", f"{workId}.gif")
    job_worker3 = log_queue.enqueue(update__done_status, 2, workId, filename)


def get_url():
    return minio.get_gif_urls()

def get_cur():
    return int(redis_conn.get("current_job_id"))


def update__done_status(worker, workId, videonames):
    if worker == 1:
        redis_conn.set(workId, ["Extracted >> composing", videonames])
    else:
        redis_conn.set(workId, ["Job Completed", videonames])
    print(f"Worker {worker} Done Task Id {workId}")

def update_fail_status(workId):
    redis_conn.set(workId, ["Failed", videonames])