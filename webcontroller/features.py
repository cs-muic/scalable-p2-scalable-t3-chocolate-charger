from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio
import subprocess
from redisConnection import redis_conn, extract_queue, compose_queue, log_queue


def frames_extraction_by2queues(filename, workId): 
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
    redis_conn.set(workId, "Extracted Done >> Now Composing")
    # push to queue 2
    job_worker2 = compose_queue.enqueue(image_compose, workId)


def image_compose_by2queues(workId):
    # download all frames
    print(f"Start Composing {workId}")
    minio.download_extracted_frames(workId)
    # perfrom sh script
    process = subprocess.Popen(f'sh ./scripts/compose.sh ./download/{workId} output.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(f"Done {workId}")
    # update state of the job
    redis_conn.set(workId, "Job Completd")

######################### Below this line Using 3 queue (The thrid is Log queue) ################################

def frames_extraction(filename, workId): 
    # pull video from minio
    print(f"Start extracting {workId}")
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


def image_compose(workId):
    # download all frames
    print("1111111111111111111231242151251262156125125125215125215125125")
    print(f"Start Composing {workId}")
    minio.download_extracted_frames(workId)
    # perfrom sh script
    process = subprocess.Popen(f'sh ./scripts/compose.sh ./download/{workId} {workId}.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(f"Done {workId}")
    # update state of the job
    minio.upload_gif(".", f"{workId}.gif")
    job_worker3 = log_queue.enqueue(update__done_status, 2, workId)

def update__done_status(worker, workId):
    if worker == 1:
        redis_conn.set(workId, "Extracted >> composing")
    else:
        redis_conn.set(workId, "Job Completed")
    print(f"Worker {worker} Done Task Id {workId}")

def update_fail_status(workId):
    redis_conn.set(workId, "BOOOOOM!!!!!!!")
