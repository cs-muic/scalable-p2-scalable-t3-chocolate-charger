from xmlrpc.client import ResponseError
import os
from minio import Minio
from minio.error import S3Error

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_ADDRESS = os.getenv("MINIO_ADDRESS")
MINIO_PORT =os.getenv("MINIO_PORT")
address = str(MINIO_ACCESS_KEY) + ":" + str(MINIO_PORT)
class minioController:
    def __init__(self):
        self.client = Minio(
        address,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure= False
    )


    # list of all bucket name
    def list_buckets(self):
        buckets = self.client.list_buckets()
        lst = [bucket.name for bucket in buckets]
        return lst

    # return all obj in the bucket
    def list_objects(self, bucket_name):
        objs = self.client.list_objects(bucket_name)
        lst = [obj.object_name for obj in objs]
        return lst

    def upload_folder(self, filePath, filename):
        found = self.client.bucket_exists("frames")
        if not found:
            self.client.make_bucket("frames")
        else:
            print("Bucket 'frames' already exists")
        # TODO: can we upload the whole folder at once? (performance issue)
        for i in range(1,51):
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
        self.client.fput_object(
            "video", filename, filePath
        )

    def upload_gif(self, filePath, filename):
        found = self.client.bucket_exists("gif")
        if not found:
            self.client.make_bucket("gif")
        else:
            print("Bucket 'gif' already exists")
        self.client.fput_object(
            "gif", filename, filePath
        )

    # list of all bucket name
    def list_buckets(self):
        buckets = self.client.list_buckets()
        lst = [bucket.name for bucket in buckets]
        return lst

    # return all obj in the bucket
    def list_objects(self, bucketname):
        objs = self.client.list_objects(bucketname)
        lst = [obj.object_name for obj in objs]
        return lst
    
    # it only download in "video" bucket
    def download_video(self, videoname):
        self.client.fget_object("video", videoname, f"./temp/{videoname}", request_headers=None)
    
    def download_extracted_frames(self, foldername):
        for i in range(1, 51):
          self.client.fget_object("frames", f"{foldername}/image{i}.jpeg", f"./download/{foldername}/image{i}.jpeg", request_headers=None)

    # in case we want to download something outside the bucket we controlled
    def download_specific_file(self, bucket, object, name):
        self.client.fget_object(bucket, object, name)

minio = minioController()

