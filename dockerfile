#FROM ubuntu:18.04
FROM python:3.9

# install ffmpeg on our ubuntu
#WORKDIR /app
#ENV DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && apt-get install -y ffmpeg

# also install imagemagick
#RUN apt install imagemagick -y
# COPY ./sample.mp4 /
#COPY ./script.sh /
#RUN chmod +x /script.sh
#ENTRYPOINT ["/script.sh"]
#CMD ["input.mp4", "output.mp4"]

# for flask

ADD webcontroller /app 
RUN pip install poetry


COPY webcontroller/pyproject.toml webcontroller/poetry.lock ./
RUN poetry install --no-root --no-dev

COPY webcontroller ./
RUN poetry install --no-dev


CMD [ "poetry", "run" , "gunicorn", "-w", "2", "--threads", "2", "-b", "0.0.0.0:5000", "app:app" ]

