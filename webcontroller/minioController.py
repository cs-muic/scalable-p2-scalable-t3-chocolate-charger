from xmlrpc.client import ResponseError
import os
from minio import Minio
from minio.error import S3Error

class minioController:
    def __init__(self):
        self.client = Minio(
        "localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure= False
    )

    def upload_folder(self, filePath, filename):
        found = self.client.bucket_exists("frames")
        if not found:
            self.client.make_bucket("frames")
        else:
            print("Bucket 'frames' already exists")
        # TODO: change this "temp.mp4"

        for i in range(1,201):
            self.client.fput_object(
                "frames", f"{filename}/image{i}.jpeg", f"{filePath}/image{i}.jpeg"
            )
        print("DONE UPLOAD====================================")

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
            print(bucket)
    
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

minio = minioController()

