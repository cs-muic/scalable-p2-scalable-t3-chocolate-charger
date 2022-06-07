from xmlrpc.client import ResponseError
from minio import Minio
from minio.error import S3Error

import time
from rq import get_current_job

class minioController:
    def __init__(self):
        self.client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure= False
    )

    def upload_video(self, file):
        found = self.client.bucket_exists("video")
        if not found:
            self.client.make_bucket("video")
        else:
            print("Bucket 'video' already exists")

        # TODO: change this "temp.mp4"
        self.client.fput_object(
            "video", "temp.mp4", file
        )
    
    def list_buckets(self):
        buckets = self.client.list_buckets()
        for bucket in buckets:
            print(bucket.name, bucket.creation_date)
            print("==================")
            print(bucket)
            print("==================")
    
    def download_objects(self, bucketname):
        objs = self.client.list_objects(bucketname)
        for obj in objs:
            print(obj.object_name)
            self.client.fget_object(bucketname, obj.object_name, "./download/kenny.mp4", request_headers=None)
            # try:
            #     response = self.client.get_object(bucketname, obj)
            #     # Read data from response.
            # finally:
            #     response.close()
            #     response.release_conn()
            # try:
            #     print(self.client.fget_object(bucketname, obj, './download/'))
            # except ResponseError as err:
            #     print(err) #eieiei

    def get_file(self, bucket, object, name):
        self.client.fget_object(bucket, object, name)

def temp():
    job = get_current_job()
    time.sleep(10)

    return {
        "job_id": job.id
    }


# def get_object(bucket, object, name):
