import uvicorn
from fastapi import FastAPI, File, UploadFile
import json

from feature_embedding import embedder, read_imagefile, config_model


api_embedder = FastAPI(title='API Embedder')

global model, cfg

@api_embedder.post("/api_embedder")
async def embedder_api(file: UploadFile = File(...)):
	image = read_imagefile(file.file.read())
	embedded_img = embedder(model, cfg, image)
	json_embedded_img = json.dumps(embedded_img)

	return json_embedded_img


if __name__ == "__main__":
	#Init Retina Model
	model, cfg = config_model()

	# host = 'localhost' if run local else 'embedder'
	uvicorn.run(api_embedder, port=1000, host='localhost', debug=True)