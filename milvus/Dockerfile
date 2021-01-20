#FROM ubuntu:20.04
FROM python:3.6.8

# Copy current dir contents to /core
COPY . /milvus

WORKDIR /milvus

RUN pip install --upgrade pip
#RUN pip3 install -r requirements.txt

RUN pip install python-multipart
RUN pip install pymilvus==0.2.14
RUN pip install fastapi
RUN pip install uvicorn
#RUN pip install ast

EXPOSE 3000

# command to run on container start
CMD [ "python", "./api_milvus.py" ]