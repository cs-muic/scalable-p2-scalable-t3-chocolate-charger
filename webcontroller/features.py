from minio import Minio
from minio.error import S3Error


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