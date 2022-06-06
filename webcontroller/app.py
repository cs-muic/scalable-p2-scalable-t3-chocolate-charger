import os
from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
from flask_minio import Minio



app = Flask(__name__)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

storage = Minio(app)

app.config

client = Minio(
    "play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)

# # Make 'videos' bucket if not exist.
# found = client.bucket_exists("videos")
# if not found:
#     client.make_bucket("videos")
# else:
#     print("Bucket 'videos' already exists")
#
# found = client.bucket_exists("frames")



@app.route('/api/submit', methods=['POST'])
def submit():
    #create a job and add to the queue
    return jsonify({"WTF":"WTF"}), 200

@app.route('/api/list/<', methods=['GET'])
def list():
    #lists all GIF images in a bucket
    lst = []
    return jsonify({"WTF":"WTF"}), 200


if __name__ == '__main__':
    app.run()
