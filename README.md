## Milestone 1

### HOW TO RUN M1
```
docker build -f Dockerfile -t p2-test .
docker run -v /Users/marcmarkcat/Desktop/Study/scalable/P2/scalable-p2-scalable-t3-chocolate-charger:/app  p2-test sample.mp4 output.gif
```

## Milestone 2 

### What I have done: 

added minio configmap to store some minio access key and minio secret key
started webcontroller component (REST API) using flask
    : trying to grab minio environment using python's os
    : create_bucket via python
    : Fix Dockerfile to work with python 