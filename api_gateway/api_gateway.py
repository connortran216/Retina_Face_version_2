import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
import requests
import ast

api_gateway = FastAPI(title='API Gateway')

global url

@api_gateway.post("/api_gateway_insert")
async def insert(id: str = Form(...), file: UploadFile = File(...)):

	data = {
		'id': id
	}
	files = [
		('file', file.file)
	]
	headers = {}

	insert_response = requests.request("POST", url[0], headers=headers, data=data, files=files)

	json_insert = insert_response.content.decode("utf-8")
	json_insert = ast.literal_eval(json_insert)

	#return json_insert
	res = {
		"Message": json_insert['Message'],
		"status": 200
	}

	return res


@api_gateway.post("/api_gateway_search")
async def search(file: UploadFile = File(...)):

	data = {}
	files = [
		('file', file.file)
	]
	headers = {}

	search_response = requests.request("POST", url[1], headers=headers, data=data, files=files)

	json_search = search_response.content.decode("utf-8")
	json_search = ast.literal_eval(json_search)

	return json_search


@api_gateway.post("/api_gateway_create")
async def create(_id: str = Form(...), title: str = Form(...), name: str = Form(...)):

	data = {
		"_id": _id,
		"title": title,
		"name": name
	}

	headers = {}

	create_response = requests.request("POST", url[2], headers=headers, data=data)

	json_create = create_response.content.decode("utf-8")
	json_create = ast.literal_eval(json_create)


	res = {
		"Record ID": json_create["Record ID"],
		"status": 200
	}

	return res


@api_gateway.post("/api_gateway_delete_collection")
async def delete_collection():

	data = {}

	headers = {}

	create_response = requests.request("POST", url[3], headers=headers, data=data)

	json_delete = create_response.content.decode("utf-8")
	json_delete = ast.literal_eval(json_delete)


	res = {
		"Message": json_delete["result"],
		"status": 200
	}

	return res


@api_gateway.post("/api_gateway_delete_by_id")
async def delete_by_id(id: str = Form(...)):
	data = {
		"id": id
	}

	headers = {}

	create_response = requests.request("POST", url[4], headers=headers, data=data)

	json_delete = create_response.content.decode("utf-8")
	json_delete = ast.literal_eval(json_delete)

	res = {
		"Message": json_delete["result"],
		"status": 200
	}

	return res

if __name__ == "__main__":
	#URL
	url = [
		"http://core:8000/core_insert",
		"http://core:8000/core_search",
		"http://core:8000/core_create",
		"http://core:8000/core_delete_collection",
		"http://core:8000/core_delete_by_id"
	]

	# host = 'localhost' if run local else 'api_gateway'
	uvicorn.run(api_gateway, port=8888, host='api_gateway', debug=True)