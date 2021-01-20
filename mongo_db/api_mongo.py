import uvicorn
from fastapi import FastAPI, Form
from pymongo import MongoClient


api_mongo = FastAPI(title='Mongo Database')

global client, database, collection

@api_mongo.post("/create_mongo_db")
async def create_new_employee(_id: str = Form(...), title: str = Form(...), name: str = Form(...)):

	# IDs, Name, Title
	employee = {
		"_id": _id,
		"title": title,
		"name": name
		}
	record = collection.insert(employee)

	return record

@api_mongo.post("/search_mongo_db")
async def search_name(_id: str = Form(...)):

	# IDs, Name, Title
	result = collection.find_one(
		{
			"_id": _id
		}
	)
	if result is not None:
		name = result.get('name')
		return name

	else:
		return "No ID is found"

if __name__ == "__main__":

	# Step 1: Connect to MongoDB - Note: Change connection string as needed ##"mongodb://mongodb_net:27017"
	client = MongoClient("mongodb://mongo_db:27017")
	database = client['DPS']
	collection = database['employee_info']

	# host = 'localhost' if run local else 'api_mongo'
	uvicorn.run(api_mongo, port=1000, host='api_mongo', debug=True)