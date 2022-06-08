from fileinput import filename
import os
from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
from flask_minio import Minio
from features import *
from redisConnection import extract_queue
from minioController import minio
from rq.job import Job
import redis
from rq import Queue
# from webcontroller.features import frames_extraction 

app = Flask(__name__)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
# REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# REDIS_PORT = os.getenv("REDIS_PORT", "6379")
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

class Pocket:
    def __init__(self, filename, path, minio):
        self.filename = filename
        self.path = path
        self.jobId = -1 # before entering the queue
        self.minio = minio
    


# minio = minioController()

# redis_connection = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
# )

# extract_queue = Queue('worker1', connection=redis_connection)
# make_gif_queue = Queue('worker2', connection=redis_connection)

# CHECKING REDIS CONNECTION, DON'T DELETE
# try:
#     response = redis_connection.client_list()
#     print(response)
# except redis.ConnectionError:
#     #your error handlig code here 
#     print("error")

@app.route('/api/make_gif', methods=['POST'])
def make_gif():
    uploaded_path = request.json.get("path", None)
    uploaded_filename = request.json.get("filename", None)
    pocket = Pocket(filename=uploaded_filename, path=uploaded_path, minio=minio)
    minio.upload_video(pocket.path, pocket.filename)
    # job = extract_queue.enqueue(frames_extraction, pocket)
    job = extract_queue.enqueue(some_long_function, pocket)
    return jsonify({"OK": "DONE"}), 200


# @app.route('/api/submit', methods=['POST'])
# def submit():
#     #create a job and add to the queue
#     return jsonify({"NOT":"DONE"}), 200

# @app.route('/api/list', methods=['GET'])
# def list():
#     #lists all GIF images in a bucket
#     lst = []
#     return jsonify({"NOT":"DONE"}), 200

# @app.route('/api/upload', methods=['POST'])
# def upload():
#     path = request.json.get("path", None)
#     minio.upload_video(path)
#     return jsonify({"OK": "DONE"}), 200

@app.route('/api/listbucket', methods=['POST'])
def listing_buckets():
    # path = request.json.get("path", None)
    minio.list_buckets()
    return jsonify({"OK": "listing"}), 200

# @app.route('/api/listobject', methods=['POST'])
# def listing_object():
#     # path = request.json.get("path", None)
#     minio.download_objects("video")
#     return jsonify({"OK": "listing"}), 200





if __name__ == '__main__':
    app.run()