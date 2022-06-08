from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio

def notify_queue(str):
    print(str)

def frames_extraction(filename): 

    job = get_current_job()

    minio.download_video(filename)
    path = str.split(filename, '.')[0]
    print(path)
    os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scripts/extract.sh ./temp/{filename} frames') # TOFIX: harcode and path
    print("extraction DONEEEEEEEEEEEEEE")
    minio.upload_folder("./frames", job.id)
    print("work done eieiei !!!!!")
    return path


def image_compose(jobId):
    #download all frames
    print("debugging")
    minio.download_extracted_frames(jobId)
    os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scripts/compose.sh ./temp/{filename} frames') # TOFIX: harcode and path



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
