# syntax=docker/dockerfile:1

FROM python:3.11.1-slim-buster

WORKDIR /python-docker

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN mkdir -p /app
COPY app/requirements.txt app/req.txt
RUN pip3 install -r app/req.txt

#COPY . .

#CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "app/app:app"]
