import numpy as np
from milvus import Milvus, MetricType

def init_milvus():
	# MILVUS to find vector similarity
	# Milvus server IP address and port.
	# You may need to change _HOST and _PORT accordingly.
	#_HOST = '127.0.0.1'
	_HOST = 'milvus'
	_PORT = '19530'  # default value

	# Vector parameters
	_DIM = 512  # dimension of vector

	_INDEX_FILE_SIZE = 32  # max file size of stored index

	milvus = Milvus(_HOST, _PORT, pool_size=10)

	# Create collection demo_collection if it dosen't exist.
	collection_name = 'retina_face'

	status, ok = milvus.has_collection(collection_name)
	if not ok:
		param = {
			'collection_name': collection_name,
			'dimension': _DIM,
			'index_file_size': _INDEX_FILE_SIZE,  # optional
			'metric_type': MetricType.L2  # optional
		}

		print(milvus.create_collection(param))

	return milvus


def milvus_insert_vector(milvus, vectors, id):

	feature_vectors = vectors

	id_vectors = []
	id_vectors.append(int(id))

	collection_name = 'retina_face'

	### Insert vectors into demo_collection, return status and vectors id list
	status, ids = milvus.insert(collection_name=collection_name, records=feature_vectors, ids=id_vectors)
	if not status.OK():
		print("Insert failed: {}".format(status))
	else:
		print(ids)

	# Flush collection  inserted data to disk.
	milvus.flush([collection_name])

	return status, ids


def milvus_search_vector(milvus, vectors):

	feature_vectors = vectors

	collection_name = 'retina_face'

	# execute vector similarity search
	search_param = {
		"nprobe": 16
	}

	print("Searching ... ")

	param = {
		'collection_name': collection_name,
		'query_records': [feature_vectors[0]],
		'top_k': 10,
		'params': search_param,
	}

	status, results = milvus.search(**param)

	new_result = []

	if status.OK():
		print("RESULT: ", results[0][0])
		for row in results:
			for item in row:
				new_result.append(item)
		return new_result[0]
	else:
		print("Search failed !!! ", status)
		return None


def milvus_delete_vector_by_ids(milvus, id):
	# Define collection name
	collection_name = 'retina_face'

	# append ID to list for milvus requirement
	id_vectors = []
	id_vectors.append(int(id))

	# Delete vector by ID
	result = milvus.delete_entity_by_id(collection_name='retina_face', id_array=id_vectors)

	# Flush collection  inserted data to disk.
	milvus.flush([collection_name])

	return result


def milvus_delete_collection(milvus):
	# Define collection name
	collection_name = 'retina_face'

	###Delete demo_collection
	result = milvus.drop_collection(collection_name)

	# Flush collection inserted data to disk.
	milvus.flush([collection_name])

	return result

