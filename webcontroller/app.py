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

@app.route('/api/make_gif', methods=['POST'])
def make_gif():

    # create uqiue job ID
    global init_job_id
    init_job_id += 1
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
    

# api that return a list of buckets (name)
@app.route('/api/listbucket', methods=['POST'])
def listing_buckets():
    lst = minio.list_buckets()
    return json.dumps(lst), 200


if __name__ == '__main__':
    app.run()