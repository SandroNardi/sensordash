# syntax=docker/dockerfile:1

FROM python:3.11.1-slim-buster

WORKDIR /python-docker

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN mkdir -p /app
RUN mkdir -p /base

COPY app/requirements.txt base/requirements.txt
#RUN pip3 install -r requirements.txt

#COPY . .

#CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "app/app:app"]
