#CORE DOCKERFILE
# Use official python runtime
FROM python:3.6.8
#FROM ubuntu:20.04

# Copy current dir contents to /core
COPY . /kafka_consumer

#Set working directory
WORKDIR /kafka_consumer

#ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	tk-dev apt-utils python3-pip tzdata locales

# create alias
RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip


RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

RUN pip install python-multipart
RUN pip install requests
RUN pip install kafka-python


# command to run on container start
CMD [ "python", "kafka_consumer.py" ]