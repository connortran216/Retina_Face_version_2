#CORE DOCKERFILE
# Use official python runtime
FROM python:3.6.8
#FROM ubuntu:20.04

# Copy current dir contents to /core
COPY . /embedder

#Set working directory
WORKDIR /embedder


#ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	tk-dev apt-utils python3-pip tzdata locales

# create alias
RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip


RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y


COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install kafka-python

EXPOSE 1000

# command to run on container start
CMD [ "python", "kafka_embedder.py" ]