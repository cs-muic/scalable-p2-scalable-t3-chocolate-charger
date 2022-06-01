FROM ubuntu:18.04

# install ffmpeg on our ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg

# also install imagemagick
RUN apt install imagemagick -y

COPY ./script.sh /
RUN chmod +x /script.sh
ENTRYPOINT ["/script.sh"]
CMD ["input.mp4", "output.mp4"]

#################################
# Waste (in case we change ubuntu version)
# FROM ubuntu:15.10
# RUN sudo apt update
# RUN sudo add-apt-repository ppa:djcj/hybrid
# RUN sudo apt-get update
# RUN sudo apt-get install ffmpeg
#######
# RUN apt-get -y update
# RUN apt-get -y upgrade
# RUN apt-get install -y ffmpeg
# RUN apk --update add imagemagick
######
# RUN add-apt-repository ppa:mc3man/trusty-media
# RUN apt-get update
# RUN apt-get dist-upgrade
# RUN apt-get install ffmpeg