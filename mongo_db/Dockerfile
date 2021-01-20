#MONGO DOCKERFILE
FROM python:3.6.8

# Copy current dir contents to /core
COPY . /mongo_db

WORKDIR /mongo_db

RUN apt-get update && apt-get install -y \
	tk-dev apt-utils python3-pip tzdata locales

# create alias
RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip


RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
#RUN pip3 install -r requirements.txt

RUN pip install uvicorn
RUN pip install fastapi
RUN pip install pymongo
RUN pip install python-multipart
#RUN pip install ast

EXPOSE 1000
EXPOSE 27017
# command to run on container start
CMD [ "python", "./api_mongo.py" ]