from concurrent.futures.thread import _worker
from fileinput import filename
import os
from unicodedata import name
from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
from flask_minio import Minio
from features import *  # TOFIX: this
from redisConnection import redis_conn, extract_queue, compose_queue, log_queue
from minioController import minio
from rq.job import Job
import redis
from rq import Connection, Queue, Worker
import json

app = Flask(__name__)

### Debugging ###
# MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "localhost:9000")
# MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
# MINIO_ADDRESS = os.getenv("MINIO_ADDRESS")
# REDIS_HOST = os.getenv("REDIS_HOST", "redis://localhost")
# REDIS_PORT = os.getenv("REDIS_PORT", "6379")
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# job id counter
# we also store this id in the redis
redis_conn.set("current_job_id", "0")
init_job_id = 0


@app.route('/api/make_gifs', methods=['POST'])
def make_gifs():
    bucket_name = request.json.get("bucket", None) #retrieve bucket name
    objects = minio.list_objects(bucket_name) #get all objects
    for obj in objects:
        job_worker1 = extract_queue.enqueue(frames_extraction, obj, bucket_name)
        job_id = job_worker1.id
        job_worker2 = compose_queue.enqueue(image_compose, job_id, depends_on=job_worker1)

    return jsonify({"bucket": bucket_name, "status": "working", "job_id":job_id}), 200
 
@app.route('/api/make_gif', methods=['POST'])
def make_gif():
    # create unqiue job ID
    init_job_id = int(redis_conn.get("current_job_id"))
    redis_conn.set("current_job_id", str(init_job_id + 1))
    # set its state to redis

    redis_conn.set(init_job_id, "Extracting Frames")
    uploaded_filename = request.json.get("filename", None)

    # test
     
    # pass it to worker 1 (enqueue)
    job_worker1 = extract_queue.enqueue(frames_extraction,uploaded_filename, init_job_id)
    # return job's ID that we can use it to check the status
    return jsonify({"jobId": init_job_id}), 200

@app.route('/api/make_gif_upload', methods=['POST'])
def make_gif_upload():
    # create uqiue job ID
    init_job_id = int(redis_conn.get("current_job_id"))
    redis_conn.set("current_job_id", str(init_job_id + 1))
    # set its state to redis
    redis_conn.set(init_job_id, "Extracting Frames")

    uploaded_path = request.json.get("path", None)
    uploaded_filename = request.json.get("filename", None)

    # upload that video
    minio.upload_video(uploaded_path, uploaded_filename)
    # pass it to worker 1 (enqueue)
    job_worker1 = extract_queue.enqueue(frames_extraction,uploaded_filename, init_job_id)
    # return job's ID that we can use it to check the status
    return jsonify({"jobId": init_job_id}), 200

@app.route('/api/status', methods=['POST'])
def check_status():
    job_id = request.json.get("jobId", None)
    process = redis_conn.get(job_id)
    print(str(process))
    return jsonify({"process": str(process)}), 200
    

# api that return a list of objects
@app.route('/api/list_objs', methods=['POST'])
def list_objects():
    bucket_name = request.json.get("bucket", None)
    lst = minio.list_objects(bucket_name)
    return json.dumps(lst), 200

# creates multiple jobs for all videos in the bucket
@app.route('/api/doing_bucket', methods=['POST'])
def do_bucket():
    bucket_name = request.json.get("bucket", None)
    lst = minio.list_objects(bucket_name)
    to_return = dict()

    
    for i in range(len(lst)):
        # tracking job Id
        init_job_id = int(redis_conn.get("current_job_id"))
        redis_conn.set("current_job_id", str(init_job_id + 1))
        # enqueue to worker1
        job_worker1 = extract_queue.enqueue(frames_extraction,lst[i], init_job_id)
        to_return[lst[i]] = init_job_id
    
    
    return json.dumps(to_return), 200

# api that return a list of buckets (name)
@app.route('/api/list_bucket', methods=['POST'])
def list_buckets():
    lst = minio.list_buckets()
    return json.dumps(lst), 200

################ Testing API ###################
@app.route('/api/testing', methods=['POST'])
def testing():
    lst = [1,2,3]
    return json.dumps(lst), 200

if __name__ == '__main__':
    app.run()