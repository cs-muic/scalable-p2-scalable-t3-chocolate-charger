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
    job_worker1 = extract_queue.enqueue(frames_extraction, pocket.filename)
    job_id1 = job_worker1.id
    #job_worker2 = compose_queue.enqueue(notify_queue, job_worker1.id, depends_on=job_worker1)
    # workers = Worker.all(queue=extract_queue)
    # workers.work()
    
    # w = Worker([extract_queue], connection=redis_conn)
    # try:
    #     w.work()
    # except:
    #     print("An exception occurred")
    print(job_worker1.get_status())
    return jsonify({"job": job_id1}), 200


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
