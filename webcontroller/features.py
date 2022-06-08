from xmlrpc.client import ResponseError
import os
from minio import Minio
from minio.error import S3Error
import time
from rq import get_current_job
# from app import extract_queue, make_gif_queue

class minioController:
    def __init__(self):
        self.client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure= False
    )

    def upload_video(self, filePath, filename):
        found = self.client.bucket_exists("video")
        if not found:
            self.client.make_bucket("video")
        else:
            print("Bucket 'video' already exists")
        # TODO: change this "temp.mp4"
        self.client.fput_object(
            "video", filename, filePath
        )
    
    def list_buckets(self):
        buckets = self.client.list_buckets()
        for bucket in buckets:
            print(bucket.name, bucket.creation_date)
            print("==================")
            print(bucket)
            print("==================")
    
    def download_video(self, videoname):
        self.client.fget_object("video", videoname, f"./download/{videoname}", request_headers=None)

    def download_extracted_frames(self, bucketname):
        objs = self.client.list_objects(bucketname)
        for obj in objs:
            print(obj.object_name)
            self.client.fget_object(bucketname, obj.object_name, "./download/kenny.mp4", request_headers=None)

    # in case we want to download something outside the bucket we controlled
    def download_specific_file(self, bucket, object, name):
        self.client.fget_object(bucket, object, name)

def notify_queue():
    pass

def frames_extraction(pocket):
    print("hahaha")
    pocket.minio.download_video(pocket.filename)
    os.popen(f'sh /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger/scipt.sh ./download/{pocket.filename} out.gif') # TOFIX: harcode and path

def temp():
    job = get_current_job()
    time.sleep(10)

    return {
        "job_id": job.id
    }


import time

from rq import get_current_job


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
# def get_object(bucket, object, name):
