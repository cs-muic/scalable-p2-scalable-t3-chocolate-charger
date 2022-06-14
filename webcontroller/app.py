from concurrent.futures.thread import _worker
from fileinput import filename
import os
from unicodedata import name
from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
#from flask_minio import Minio
from flask_cors import CORS
from features import *  # TOFIX: this
from redisConnection import redis_conn, extract_queue, compose_queue, log_queue
from minioController import minio
from rq.job import Job
import redis
from rq import Connection, Queue, Worker
import json


app = Flask(__name__)
CORS(app)

# job id counter
# we can also store this id in the redis
redis_conn.set("current_job_id", "0")
init_job_id = int(redis_conn.get("current_job_id"))
 
@app.route('/api/make_gif', methods=['POST'])
def make_gif():
    # create unqiue job ID
    init_job_id = int(redis_conn.get("current_job_id"))
    redis_conn.set("current_job_id", str(init_job_id + 1))
    # set its state to redis

    uploaded_filename = request.json.get("filename", None)
    redis_conn.set(init_job_id, f"Extracting Frames, {uploaded_filename}")

    # pass it to worker 1 (enqueue)
    job_worker1 = extract_queue.enqueue(frames_extraction,filename=uploaded_filename, workId=init_job_id, on_failure=update_fail_status)
    # return job's ID that we can use it to check the status
    return jsonify({"jobId": init_job_id}), 200

@app.route('/api/make_gif_upload', methods=['POST'])
def make_gif_upload():
    # create uqiue job ID
    init_job_id = int(redis_conn.get("current_job_id"))
    redis_conn.set("current_job_id", str(init_job_id + 1))
    # set its state to redis
    uploaded_path = request.json.get("path", None)
    uploaded_filename = request.json.get("filename", None)
    redis_conn.set(init_job_id, f"Extracting Frames, {uploaded_filename}")
    # upload that video
    minio.upload_video(uploaded_path, uploaded_filename)
    # pass it to worker 1 (enqueue)
    job_worker1 = extract_queue.enqueue(frames_extraction,filename=uploaded_filename, workId=init_job_id, on_failure=update_fail_status)
    # return job's ID that we can use it to check the status
    return jsonify({"jobId": init_job_id,}), 200

#FIX
@app.route('/api/status', methods=['POST'])
def check_status():
    job_id = request.json.get("jobId", None)
    process = redis_conn.get(job_id)
    print(process.decode("utf-8"))
    return jsonify({"process": process.decode("utf-8")}), 200
    

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
        init_job_id = int(redis_conn.get("current_job_id"))
        redis_conn.set(init_job_id, f"Extracting Frames, {lst[i]}")
        redis_conn.set("current_job_id", str(init_job_id + 1))
        # enqueue to worker1
        job_worker1 = extract_queue.enqueue(frames_extraction,filename=lst[i], workId=init_job_id, on_failure=update_fail_status)
        to_return[lst[i]] = init_job_id
    
    
    return json.dumps(to_return), 200

@app.route('/api/get_status', methods=["GET"])
def get_status():
    cur_job_id = get_cur()
    to_return = []
    for job_id in range(cur_job_id):
        process = str(redis_conn.get(job_id).decode("utf-8"))
        to_return.append(str(job_id) +": " + process)
    return json.dumps(to_return)

# return all urls of gifs to display 
@app.route('/api/get_urls', methods=['GET'])
def get_urls():
    return json.dumps(get_url())

# api that return a list of buckets (name)
@app.route('/api/list_bucket', methods=['GET'])
def list_buckets():
    lst = minio.list_buckets()
    return json.dumps(lst), 200


if __name__ == '__main__':
    app.run()