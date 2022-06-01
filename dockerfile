FROM ubuntu:18.04

# install ffmpeg on our ubuntu
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg

# also install imagemagick
RUN apt install imagemagick -y
# COPY ./sample.mp4 /
COPY ./script.sh /
RUN chmod +x /script.sh
ENTRYPOINT ["/script.sh"]
CMD ["input.mp4", "output.mp4"]

<<<<<<< HEAD
#################################
=======
>>>>>>> a5eb3c3a5dd758857ccb15962e735d5cab7c6dd3
