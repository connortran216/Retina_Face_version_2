from kafka import KafkaConsumer
import requests
import ast
import logging

### Global variables
global url
global consumer


def consumer_response(consumer):

	for message in consumer:
		consumer.commit()
		data = message.value.decode("utf-8")
		data = ast.literal_eval(data)

		if data[-1] == 'insert':
			print("Insert response Offset: ", message.offset)

			# data = message.value.decode("utf-8")
			# data = ast.literal_eval(data)
			embedded_img = ast.literal_eval(data[0].decode("utf-8"))

			id = data[1]

			data = {
				'embedded_img': str(embedded_img),
				'id': id
			}
			files = []
			headers = {}

			response = requests.request("POST", url[0], headers=headers, data=data, files=files)

			print("Request Successfully !!!")
			logging.critical("Request Successfully !!!")
			consumer.commit()

		else:
			print("Search response Offset: ", message.offset)

			data = message.value.decode("utf-8")
			embedded_img = ast.literal_eval(data)

			data = {
				'embedded_img': str(embedded_img)
			}
			files = []
			headers = {}

			response = requests.request("POST", url[1], headers=headers, data=data, files=files)

			print("Request Successfully !!!")
			logging.critical("Request Successfully !!!")
			consumer.commit()


if __name__ == "__main__":

	### Create Kafka consumer host
	consumer = KafkaConsumer('embedder_response',
							 group_id='embedder_response_group',
							 bootstrap_servers=['kafka:9093'])

	print("Finish loading Consumer !!!")
	logging.critical("Finish loading Consumer !!!")

	url = ["http://core:8000/core_insert_consumer",
		   "http://core:8000/core_search_consumer"
		   ]

	consumer_response(consumer)

