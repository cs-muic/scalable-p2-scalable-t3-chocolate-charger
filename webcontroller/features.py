from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio

def notify_queue():
    pass

def frames_extraction(filename):
    print("hahahas====================")
    # minio.download_video(filename)
    # os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scipt.sh ./download/{filename} out.gif') # TOFIX: harcode and path

def temp():
    job = get_current_job()
    time.sleep(10)

    return {
        "job_id": job.id
    }


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
