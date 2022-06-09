from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio
import subprocess
from redisConnection import redis_conn, extract_queue, compose_queue

def frames_extraction(filename, workId): 
    job = get_current_job()
    
    # pull video from minio
    minio.download_video(filename)
    path = str.split(filename, '.')[0]
    print(path)

    process = subprocess.Popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scripts/extract.sh ./temp/{filename} frames', shell=True, stdout=subprocess.PIPE)
    process.wait()

    # upload frames back to minio
    minio.upload_folder("./frames", job.id)
    print(f"extraction {job.id} done")

    #update state of the job
    redis_conn.set(workId, "Extracted >> composing")

    job_worker2 = compose_queue.enqueue(image_compose, job.id, workId)


def image_compose(jobId, workId):

    #download all frames
    print(f"Start Composing {jobId}")
    minio.download_extracted_frames(jobId)

    process = subprocess.Popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scripts/compose.sh ./download/{jobId} output.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(f"Done {jobId}")
    redis_conn.set(workId, "Job Completd")

def update_status(worker, workId):
    if worker == 1:
        redis_conn.set(workId, "Extracted >> composing")
    else:
        redis_conn.set(workId, "Job Completd")


def some_long_function(some_input):
    """An example function for redis queue."""
    job = get_current_job()
    time.sleep(10)

    print( {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    })
