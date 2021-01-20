import uvicorn
from fastapi import FastAPI, Form
import ast

from milvus_functions import init_milvus
from milvus_functions import milvus_insert_vector, milvus_search_vector

#Fast API
api_milvus = FastAPI(title='API Milvus')

global milvus

#Insert function
@api_milvus.post("/insert_api_milvus")
async def insert_api(embedded_img: str = Form(...), id: str = Form(...)):

	embedded_img = ast.literal_eval(embedded_img)

	status, ids = milvus_insert_vector(milvus, embedded_img, id)

	return status, ids

#Search function
@api_milvus.post("/search_api_milvus")
async def search_api(embedded_img: str = Form(...)):

	embedded_img = ast.literal_eval(embedded_img)

	id = milvus_search_vector(milvus, embedded_img)

	return id

if __name__ == "__main__":
	# Create Milvus model
	milvus = init_milvus()

	# host = 'localhost' if run local else 'api_milvus'
	uvicorn.run(api_milvus, port=3000, host='api_milvus', debug=True)