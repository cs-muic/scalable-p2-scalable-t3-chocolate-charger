from minio import Minio
from minio.error import S3Error
import time
from rq import get_current_job
from app import extract_queue, make_gif_queue

minio_client = Minio(
        "localhost:7000",
        access_key="minio",
        secret_key="minio123",
        secure= False
    )

def frames_extraction(video_name):
    found = minio_client.bucket_exists("frames_{video_name}")
    if not found:
        minio_client.make_bucket("frames_{video_name}")
    else:
        print("Bucket 'frames_{video_name}' already exists")

    #extracted =  # run shell script that put into a temporary folder
    folder
    minio_client.fput_object(
        "frames_{video_name}", , 
    )
    





def upload_video(file, job_num):

    found = minio_client.bucket_exists("video")
    name_minio = "video{job_num}.mp4"
    if not found:
        minio_client.make_bucket("video")
    else:
        print("Bucket 'video' already exists")

    minio_client.fput_object(
        "video", name_minio, file
    )

    return name_minio