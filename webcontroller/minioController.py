from xmlrpc.client import ResponseError
import os

from requests import request
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


    # list of all bucket name
    def list_buckets(self):
        buckets = self.client.list_buckets()
        lst = [bucket.name for bucket in buckets]
        return lst

    # return all obj in the bucket
    def list_objects(self, bucket_name):
        objs = self.client.list_objects(bucketname)
        lst = [obj.object_name for obj in objs]
        return lst

    def upload_folder(self, filePath, filename):
        found = self.client.bucket_exists("frames")
        if not found:
            self.client.make_bucket("frames")
        else:
            print("Bucket 'frames' already exists")
        # TODO: change this "temp.mp4"
        self.client.fput_object(
            "frames", filename, filePath
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
    
    
    def download_video(self, videoname):
        self.client.fget_object("video", videoname, f"./download/{videoname}", request_headers=None)

    def download_extracted_frames(self, foldername):
        #version 1 
        self.client.fget_object("frames", foldername, f"./download/{foldername}", request_headers=None)
        #version 2 
        #for i in range(1, 201):
        #   self.client.fget_object("frames", f"{foldername}/image{i}.jpeg", f"./download/{foldername}/image{i}.jpeg", request_headers=None)
    
        # for obj in objs:
        #     print(obj.object_name)
        #     self.client.fget_object(bucketname, obj.object_name, "./download/kenny.mp4", request_headers=None)

    # in case we want to download something outside the bucket we controlled
    def download_specific_file(self, bucket, object, name):
        self.client.fget_object(bucket, object, name)

minio = minioController()