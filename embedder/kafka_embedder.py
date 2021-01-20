from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import ast
import logging


from feature_embedding import config_retina_model, config_facenet_model
from feature_embedding import read_imagefile, face_extract, face_features_extraction

global retinaface, cfg
global facenet


def embedder_api(file):
	# Read image
	#time.sleep(10)
	for i in range(10000):
		continue

	image = read_imagefile(file)

	# Extract faces and features from it
	faces, img_raw = face_extract(retinaface, cfg, image)
	embedded_img = face_features_extraction(facenet, faces, img_raw)

	# Compress data
	json_embedded_img = json.dumps(embedded_img)
	bytes_embedded_img = json_embedded_img.encode('utf-8')

	return bytes_embedded_img


if __name__ == "__main__":
	# Init Retina Model (face extract)
	retinaface, cfg = config_retina_model()
	print("Finish loading RetinaFace")
	logging.critical("Finish loading RetinaFace")

	# Init Facenet model (embedder)
	facenet = config_facenet_model()
	print("Finish loading FaceNet")
	logging.critical("Finish loading FaceNet")

	# Producer host
	producer = KafkaProducer(bootstrap_servers=['kafka:9093'])


	# Consumer host
	consumer = KafkaConsumer('embedder_request',
							 group_id='embedder_group',
							 bootstrap_servers=['kafka:9093'],
							 auto_offset_reset='latest',
							 session_timeout_ms = 20000,
							 heartbeat_interval_ms = 10000
							 )
	print("Finish loading Producer and Consumer !!!")
	logging.critical("Finish loading Producer and Consumer !!!")

	for message in consumer:

		consumer.commit()
		data = message.value.decode("utf-8")
		data = ast.literal_eval(data)
		# # produce keyed messages to enable hashed partitioning
		if data[-1] == 'insert':
			print("Insert Offset: ", message.offset)
			### Data receive
			# data = message.value.decode("utf-8")
			# data = ast.literal_eval(data)

			print("Receive insert request !!!")
			logging.critical("Receive insert request !!!")

			bytes_embedded_img = embedder_api(data[0])
			consumer.commit()
			logging.critical("Embedding successfully !!!")

			### Data send
			data = [bytes_embedded_img, data[1], data[-1]]
			data = str(data)
			producer.send('embedder_response', value=bytes(data, 'utf-8'))
			producer.flush()

			print("Send insert response !!!")
			logging.critical("Send insert response !!!")

		else:
			print("Search Offset: ", message.offset)
		#if data[-1] == 'search':
			### Data receive
			#bytes_embedded_img = message.value
			bytes_embedded_img = data[0]

			print("Receive search request !!!")
			logging.critical("Receive search request !!!")

			bytes_embedded_img = embedder_api(bytes_embedded_img)
			# consumer.commit()
			logging.critical("Embedding successfully !!!")

			### Data send
			producer.send('embedder_response', value=bytes_embedded_img)
			producer.flush()

			print("Send search response !!!")
			logging.critical("Send search response !!!")




