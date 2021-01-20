from __future__ import print_function

from io import BytesIO

from PIL import Image
import cv2
from facenet_pytorch import InceptionResnetV1

import numpy as np
import torch
import torch.backends.cudnn as cudnn

from milvus import Milvus, IndexType, MetricType, Status

from data import cfg_re50
from layers.functions.prior_box import PriorBox
from models.retinaface import RetinaFace
from utils.box_utils import decode, decode_landm
from utils.nms.py_cpu_nms import py_cpu_nms
from utils.timer import Timer


def image_preprocessing(image):
	img_raw = image

	img = np.float32(img_raw)

	# testing scale
	target_size = 1600
	max_size = 2150
	im_shape = img.shape
	im_size_min = np.min(im_shape[0:2])
	im_size_max = np.max(im_shape[0:2])
	resize = float(target_size) / float(im_size_min)

	# prevent bigger axis from being more than max_size:
	if np.round(resize * im_size_max) > max_size:
		resize = float(max_size) / float(im_size_max)

	if True:
		resize = 1

	if resize != 1:
		img = cv2.resize(img, None, None, fx=resize, fy=resize, interpolation=cv2.INTER_LINEAR)

	im_height, im_width, _ = img.shape
	scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])

	img -= (104, 117, 123)
	img = img.transpose(2, 0, 1)
	img = torch.from_numpy(img).unsqueeze(0)

	return img, scale, im_height, im_width, resize


def face_extract(retinaface, cfg, image: Image.Image):

	cudnn.benchmark = True
	device = torch.device("cpu" if True else "cuda")
	retinaface = retinaface.to(device)

	#Resize small image
	if image.shape[0] < 300 or image.shape[1] < 300:
		dim = (500, 500)
		image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
	elif image.shape[0] > 2000 or image.shape[1] > 2000:
		dim = (1500, 1500)
		image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

	img_raw = image
	image, scale, im_height, im_width, resize = image_preprocessing(image)

	image = image.to(device)
	scale = scale.to(device)

	_t = {'forward_pass': Timer(), 'misc': Timer()}

	_t['forward_pass'].tic()

	loc, conf, landms = retinaface(image)  # forward pass

	_t['forward_pass'].toc()
	_t['misc'].tic()

	priorbox = PriorBox(cfg, image_size=(im_height, im_width))
	priors = priorbox.forward()
	priors = priors.to(device)
	prior_data = priors.data

	boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
	boxes = boxes * scale / resize
	boxes = boxes.cpu().numpy()

	scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
	landms = decode_landm(landms.data.squeeze(0), prior_data, cfg['variance'])
	scale1 = torch.Tensor([image.shape[3], image.shape[2], image.shape[3], image.shape[2],
	                       image.shape[3], image.shape[2], image.shape[3], image.shape[2],
	                       image.shape[3], image.shape[2]])
	scale1 = scale1.to(device)

	landms = landms * scale1 / resize
	landms = landms.cpu().numpy()

	# ignore low scores
	inds = np.where(scores > 0.02)[0]
	boxes = boxes[inds]
	landms = landms[inds]
	scores = scores[inds]

	# keep top-K before NMS
	order = scores.argsort()[::-1]
	# order = scores.argsort()[::-1][:args.top_k]
	boxes = boxes[order]
	landms = landms[order]
	scores = scores[order]

	# do NMS
	dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
	keep = py_cpu_nms(dets, 0.4)
	# keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
	dets = dets[keep, :]
	landms = landms[keep]

	dets = np.concatenate((dets, landms), axis=1)
	_t['misc'].toc()

	return dets, img_raw
	# vectors = face_features_extraction(dets, img_raw)
	#
	# return vectors


def face_features_extraction(facenet, dets, img_raw):
	# Define variables
	bboxs = dets

	vectors = []
	cropped_img = []

	# process each face in faces
	for box in bboxs:
		x = int(box[0])
		y = int(box[1])
		w = int(box[2]) - int(box[0])
		h = int(box[3]) - int(box[1])

		confidence = str(box[4])

		if box[4] < 0.5:
			continue

		# crop face
		face = img_raw[y:y + h, x:x + w]

		input_img = torch.from_numpy(face).permute(2, 0, 1).unsqueeze(0)
		input_img = input_img.float()

		# extract features
		img_embedding = facenet(input_img)

		vectors.append(img_embedding)
		#PIL_image = Image.fromarray(face)

		feature_vectors = []
		for ten in vectors:
			feature_vectors.append(ten.tolist()[0])

		return feature_vectors

def read_imagefile(file) -> Image.Image:
	image = Image.open(BytesIO(file))
	image = np.array(image)

	return image


def check_keys(model, pretrained_state_dict):
	ckpt_keys = set(pretrained_state_dict.keys())
	model_keys = set(model.state_dict().keys())
	used_pretrained_keys = model_keys & ckpt_keys
	unused_pretrained_keys = ckpt_keys - model_keys
	missing_keys = model_keys - ckpt_keys
	assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'

	return True


def remove_prefix(state_dict, prefix):
	''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
	f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x

	return {f(key): value for key, value in state_dict.items()}


def load_model(model, pretrained_path, load_to_cpu):
	print('Loading pretrained model from {}'.format(pretrained_path))

	if load_to_cpu:
		pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
	else:
		device = torch.cuda.current_device()
		pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
	if "state_dict" in pretrained_dict.keys():
		pretrained_dict = remove_prefix(pretrained_dict['state_dict'], 'module.')
	else:
		pretrained_dict = remove_prefix(pretrained_dict, 'module.')
	check_keys(model, pretrained_dict)
	model.load_state_dict(pretrained_dict, strict=False)

	return model


def config_retina_model():
	torch.set_grad_enabled(False)
	cfg = cfg_re50

	### Retinaface for face cropping
	retinaface = RetinaFace(cfg=cfg, phase='test')
	retinaface = load_model(retinaface, './weights/Resnet50_Final.pth', True)
	retinaface.eval()
	#print('Finished loading model!')

	return retinaface, cfg

def config_facenet_model():
	### Facenet for features extraction
	facenet = InceptionResnetV1(pretrained='vggface2').eval()

	return facenet
