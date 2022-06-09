from xmlrpc.client import ResponseError
import os
import time
from rq import get_current_job
from minioController import minio

def notify_queue(str):
    print(str)

def image_compose(jobId):
    #download all frames
    print("debugging")
    minio.download_extracted_frames(jobId)
    #####
    process = subprocess.Popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scripts/compose.sh ./download/{jobId} output.gif', shell=True, stdout=subprocess.PIPE)
    process.wait()

def frames_extraction(obj_name, bucketname):
    minio.download_video(obj_name)
    path = str.split(obj_name, '.')[0]
    print(path)
    os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/script.sh ./download/{obj_name} {path}') # TOFIX: harcode and path
    minio.upload_folder(f"./{path}", obje_name)
    print("work done eieiei !!!!!")
    return path



def frames_extraction(filename): 
    minio.download_video(filename)
    path = str.split(filename, '.')
    print(path)
    os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/script.sh ./download/{filename} {path}') # TOFIX: harcode and path
    minio.upload_folder(f"./{path}", filename)
    print("work done eieiei !!!!!")
    return path

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
