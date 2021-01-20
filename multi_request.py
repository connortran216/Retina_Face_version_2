import requests
import threading
import base64


# from kafka import KafkaClient
# from kafka import KafkaConsumer
# from kafka import KafkaProducer
#
# # Producer host
# producer = KafkaProducer(bootstrap_servers=['localhost:9093'])
# par = producer.partitions_for("embedder_response")
# print(par)
#
# # Consumer host
# consumer = KafkaConsumer('embedder_request',
# 						 group_id='embedder_group',
# 						 bootstrap_servers=['localhost:9093'],
# 						 auto_offset_reset='latest',
# 						 session_timeout_ms = 20000,
# 						 heartbeat_interval_ms = 10000
# 						 )
#
# par = consumer.partitions_for_topic("embedder_response")
# print(par)

global url 
global file1, file2, file3, file4
global data1, data2, data3, data4


url = [
	"http://localhost:8888/api_gateway_create",
	"http://localhost:8888/api_gateway_insert",
	"http://localhost:8888/api_gateway_search",
	"http://localhost:8888/api_gateway_delete_collection",
	"http://localhost:8888/api_gateway_delete_by_id"
]

with open('a_dat.jpg', 'rb') as image_file:
	img_1 = base64.b64encode(image_file.read())

with open('a_hoa.jpg', 'rb') as image_file:
	img_2 = base64.b64encode(image_file.read())

with open('a_tho.jpg', 'rb') as image_file:
	img_3 = base64.b64encode(image_file.read())

with open('obama1.jpg', 'rb') as image_file:
	img_4 = base64.b64encode(image_file.read())

file1 = {
	'file': img_1
}

file2 = {
	'file': img_2
}

file3 = {
	'file': img_3
}

file4 = {
	'file': img_4
}


data4 = {
	'id': 100
}


data3 = {
	'id': 3
}

data2 = {
	'id': 2
}

data1 = {
	'id': 1
}



def send_search_request():

	# file1 = {
	# 	'file': open('a_dat.jpg', 'rb')
	# }
	# file2 = {
	# 	'file': open('a_hoa.jpg', 'rb')
	# }
	# file3 = {
	# 	'file': open('a_tho.jpg', 'rb')
	# }

	## search
	requests.post(url[2], files=file1)
	requests.post(url[2], files=file2)
	requests.post(url[2], files=file3)

	

def send_insert_request():

	### insert
	requests.post(url[1], data=data1, files=file1)
	requests.post(url[1], data=data2, files=file2)
	requests.post(url[1], data=data3, files=file3)


# def send_create_request():

# 	###create
# 	requests.post(url[0], )


if __name__ == "__main__":
	# creating thread
	t1 = threading.Thread(target=send_request, args=())
	t2 = threading.Thread(target=send_request, args=())
	t3 = threading.Thread(target=send_request, args=())
	t4 = threading.Thread(target=send_request, args=())
	t5 = threading.Thread(target=send_request, args=())
	t6 = threading.Thread(target=send_request, args=())

	# starting thread 1
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()
	t6.start()

	# wait until thread 1 is completely executed
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
	t6.join()

	# both threads completely executed
	print("Done!")

