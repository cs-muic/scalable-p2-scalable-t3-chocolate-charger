import os
from flask import Flask, request, jsonify, render_template, abort
from flask_caching import Cache
from flask_minio import Minio
from features import *
from rq.job import Job
import redis
from rq import Queue
from celery import Celery


app = Flask(__name__)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")


minio = minioController()

redis_connection = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
)

redis_queue = Queue(connection=redis_connection)

@app.route("/enqueue", methods=["POST"])
def enqueue():
    job = redis_queue.enqueue(temp)
    # return jsonify({"job_id": "a"})
    return jsonify({"job_id": job.id})

@app.route('/api/submit', methods=['POST'])
def submit():
    #create a job and add to the queue
    return jsonify({"NOT":"DONE"}), 200

@app.route('/api/list', methods=['GET'])
def list():
    #lists all GIF images in a bucket
    lst = []
    return jsonify({"NOT":"DONE"}), 200

@app.route('/api/upload', methods=['POST'])
def upload():
    path = request.json.get("path", None)
    minio.upload_video(path)
    return jsonify({"OK": "DONE"}), 200

@app.route('/api/listbucket', methods=['POST'])
def listing_buckets():
    # path = request.json.get("path", None)
    minio.list_buckets()
    return jsonify({"OK": "listing"}), 200

@app.route('/api/listobject', methods=['POST'])
def listing_object():
    # path = request.json.get("path", None)
    minio.download_objects("video")
    return jsonify({"OK": "listing"}), 200







if __name__ == '__main__':
    app.run()
