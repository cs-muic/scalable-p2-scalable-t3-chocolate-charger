from minio import Minio
from minio.error import S3Error


def upload_video(file):
    client = Minio(
        "play.min.io",
        access_key="minio",
        secret_key="minio123",
    )

    found = client.bucket_exists("video")
    if not found:
        client.make_bucket("video")
    else:
        print("Bucket 'video' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "video", "temp.mp4", "file",
    )