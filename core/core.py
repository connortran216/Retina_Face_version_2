import uvicorn
from fastapi import FastAPI, Form, File
from kafka import KafkaProducer, KafkaConsumer

import ast
import base64
import logging
### Mongo functions
from mongo_functions import init_mongodb, create_new_employee, search_name

### Milvus functions
from milvus_functions import init_milvus, milvus_insert_vector, milvus_search_vector
from milvus_functions import milvus_delete_vector_by_ids, milvus_delete_collection

### FAST API
core = FastAPI(title='Core')

### Global variables
global url
global milvus
global client, database, collection
global producer, consumer


# Create new user in MongoDB
@core.post("/core_create")
async def create_core(_id: str = Form(...), title: str = Form(...), name: str = Form(...)):

	record = create_new_employee(collection, _id, title, name)

	res = {
		"Record ID": record,
		"status": 200
	}

	return res


# Insert new user to Milvus
@core.post("/core_insert")
async def insert_core(file: bytes = File(...), id: str = Form(...)):
	file = base64.b64decode(file)

	data = [file, id, "insert"]
	data = str(data)
	# produce keyed messages to enable hashed partitioning
	producer.send('embedder_request', key=b'insert', value=bytes(data, 'utf-8'))
	producer.flush()

	print("Sent successfully !!!")

	res = {
		"Message": "Sent successfully",
		"status": 200
	}

	return res


# Search user in Milvus
@core.post("/core_search")
async def search_core(file: bytes = File(...)):

	#img_bytes = base64.b64decode(file)
	file = base64.b64decode(file)
	data = [file, 'search']
	data = str(data)
	### Embedding

	producer.send('embedder_request', value=bytes(data, 'utf-8'))
	producer.flush()

	print("Sent successfully !!!")

	res = {
			"Message": "Sent Successfully",
			"status": 200
		}

	return res



@core.post("/core_insert_consumer")
async def insert_consumer_core(embedded_img: str = Form(...), id: str = Form(...)):

	embedded_img = ast.literal_eval(embedded_img)

	### Milvus
	status, ids = milvus_insert_vector(milvus, embedded_img, id)
	print("Status: ", status)
	print("ID: ", ids)

@core.post("/core_search_consumer")
async def search_consumer_core(embedded_img: str = Form(...)):
	embedded_img = ast.literal_eval(embedded_img)

	_id = milvus_search_vector(milvus, embedded_img)
	_id = _id.id

	### MongoDB
	name = search_name(collection, str(_id))
	print("Name: ", name)


# Delete collection in Milvus
@core.post("/core_delete_collection")
async def delete_collection_core():
	result = milvus_delete_collection(milvus)

	res = {
		"result": result,
		"status": 200
	}

	return res


@core.post("/core_delete_by_id")
async def delete_by_id_core(id: str = Form(...)):
	result = milvus_delete_vector_by_ids(milvus, id)

	res = {
		"result": result,
		"status": 200
	}

	return res

if __name__ == "__main__":
	### URL
	url = [
		'http://embedder:1000/api_embedder'
	]


	### MongoDB
	# Create DB
	collection = init_mongodb()
	print("Finish loading MongoDB !!!")
	logging.critical("Finish loading MongoDB !!!")

	### Milvus
	# Create Milvus model
	milvus = init_milvus()
	print("Finish loading Milvus !!!")
	logging.critical("Finish loading MongoDB !!!")

	### Kafka
	# Create Kafka producer host
	producer = KafkaProducer(bootstrap_servers=['kafka:9093'])

	# # Create Kafka consumer host
	# consumer = KafkaConsumer('embedder_response',
	# 						 group_id='embedder_group',
	# 						 bootstrap_servers=['localhost:9093'])
	print("Finish loading Producer and Consumer !!!")
	logging.critical("Finish loading Producer and Consumer !!!")

	### Fast API
	# host = 'localhost' if run local else 'core'
	uvicorn.run(core, port=8000, host='core', debug=True)