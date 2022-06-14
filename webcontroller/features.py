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
    job_worker3 = log_queue.enqueue(update_done_status, worker=1, workId=workId, videonames=filename)
    # push to queue 2
    job_worker2 = compose_queue.enqueue(image_compose, workId=workId, filename=filename, job_timeout='1h', on_failure=update_fail_status)


def image_compose(workId, filename):
    # download all frames
    minio.download_extracted_frames(workId)
    # perfrom sh script
    process = subprocess.Popen(f'sh ./scripts/compose.sh ./download/{workId} {workId}.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(f"Done {workId}")
    # update state of the job and get url
    minio.upload_gif(f"./{workId}.gif", f"{workId}.gif")
    job_worker3 = log_queue.enqueue(update_done_status, worker=2, workId=workId, videonames=filename)


def get_url():
    return minio.get_gif_urls()

def get_cur():
    return int(redis_conn.get("current_job_id"))


def update_done_status(worker, workId, videonames):
    if worker == 1:
        redis_conn.set(workId, f"Extracted >> composing, {videonames}")
    else:
        redis_conn.set(workId, f"Job Completed, {videonames}")
    print(f"Worker {worker} Done Task Id {workId}")

def update_fail_status(job, connection, *args, **kwargs):
    filename = str(job.kwargs["filename"])
    workId = str(job.kwargs["workId"])
    print("work id : " + str(workId))
    print("filename :" + str(filename))
    redis_conn.set(workId, f"Failed, {filename}")

