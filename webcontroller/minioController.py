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
        print("DONE UPLOAD")

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
    
    # list of all bucket name
    def list_buckets(self):
        buckets = self.client.list_buckets()
        lst = [bucket.name for bucket in buckets]
        return lst

    # return all obj in the bucket
    def list_objects(self, bucketname):
        objs = self.client.list_objects(bucketname)
        # for obj in objs:
        #     print(obj.__dict__)
        #     print(obj.object_name)
        lst = [obj.object_name for obj in objs]
        print(lst)
        return lst
    
    # it only download in "video" bucket
    def download_video(self, videoname):
        self.client.fget_object("video", videoname, f"./temp/{videoname}", request_headers=None)
    
    def download_extracted_frames(self, foldername):
        for i in range(1, 201):
          self.client.fget_object("frames", f"{foldername}/image{i}.jpeg", f"./download/{foldername}/image{i}.jpeg", request_headers=None)


    # in case we want to download something outside the bucket we controlled
    def download_specific_file(self, bucket, object, name):
        self.client.fget_object(bucket, object, name)

minio = minioController()

