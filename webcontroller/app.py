from concurrent.futures.thread import _worker
from fileinput import filename
import os
from unicodedata import name
from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
from flask_minio import Minio
from features import *  # TOFIX: this
from redisConnection import redis_conn, extract_queue, compose_queue
from minioController import minio
from rq.job import Job
import redis
from rq import Connection, Queue, Worker
import json

app = Flask(__name__)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

# job id counter
init_job_id = 0

class Pocket:
    def __init__(self, filename, path, minio):
        self.filename = filename
        self.path = path
        self.jobId = -1 # before entering the queue
        self.minio = minio

@app.route('/api/make_gif', methods=['POST'])
def make_gif():
    uploaded_path = request.json.get("path", None)
    uploaded_filename = request.json.get("filename", None)
    pocket = Pocket(filename=uploaded_filename, path=uploaded_path, minio=minio)
    minio.upload_video(pocket.path, pocket.filename)
    job_worker1 = extract_queue.enqueue(frames_extraction, pocket.filename)
    job_id = job_worker1.id
    job_worker2 = compose_queue.enqueue(image_compose, job_id, depends_on=job_worker1)

    return jsonify({"job": job_worker2.id}), 200

@app.route('/api/make_gif2', methods=['POST'])
def make_gif2():
    global init_job_id
    init_job_id += 1
    redis_conn.set(init_job_id, "Extracting Frames")

    uploaded_path = request.json.get("path", None)
    uploaded_filename = request.json.get("filename", None)
    pocket = Pocket(filename=uploaded_filename, path=uploaded_path, minio=minio)
    minio.upload_video(pocket.path, pocket.filename)
    job_worker1 = extract_queue.enqueue(frames_extraction, pocket.filename, init_job_id)
    return jsonify({"jobId": init_job_id}), 200

@app.route('/api/status', methods=['POST'])
def check_status():
    job_id = request.json.get("jobId", None)
    process = redis_conn.get(job_id)
    print(str(process))
    return jsonify({"process": str(process)}), 200
    

# api that return a list of buckets (name)
@app.route('/api/listbucket', methods=['POST'])
def listing_buckets():
    lst = minio.list_buckets()
    return json.dumps(lst), 200

@app.route('/api/test', methods=['POST'])
def test():
    #  bucket_name = request.json.get("bucket", None)
     minio.list_objects("video")
     return jsonify({"test": "test"}), 200

@app.route('/api/make_bucket', methods=['POST'])
def make_bucket():
     bucket_name = request.json.get("bucket", None)



if __name__ == '__main__':
    app.run()