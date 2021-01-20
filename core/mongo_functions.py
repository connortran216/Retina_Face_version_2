from pymongo import MongoClient

### Init MongoDB
def init_mongodb():
	# Step 1: Connect to MongoDB - Note: Change connection string as needed ##"mongodb://mongo_db:27017"
	client = MongoClient("mongodb://mongo_db:27017")
	#client = MongoClient("localhost")
	database = client['DPS']
	collection = database['employee_info']

	return  collection

### Create new user in mongodb
def create_new_employee(collection, _id, title, name):
	result = collection.find_one(
		{
			"_id": _id
		}
	)

	if result is None:

		# IDs, Name, Title
		employee = {
			"_id": _id,
			"title": title,
			"name": name
			}
		record = collection.insert(employee)
		return record

	else:
		return "Duplicated ID"


### Search name by ID
def search_name(collection, _id):
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
