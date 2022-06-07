from minio import Minio
from minio.error import S3Error

import time
from rq import get_current_job

def temp():
    job = get_current_job()
    time.sleep(10)

    return {
        "job_id": job.id
    }

def upload_video(file):
    client = Minio(
        "localhost:7000",
        access_key="minio",
        secret_key="minio123",
        secure= False
    )

    found = client.bucket_exists("video")
    if not found:
        client.make_bucket("video")
    else:
        print("Bucket 'video' already exists")

    client.fput_object(
        "video", "temp.mp4", file
    )