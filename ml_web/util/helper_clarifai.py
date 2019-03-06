from clarifai.rest import ClarifaiApp
from app import app
import os
from clarifai.rest import Image as ClImage

app_clarifai=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])

# Clarifai - get relevant image tags based on specified Clarifai model
def predict_image_celebrity(image, model):

    model = app_clarifai.models.get(model)
    image = ClImage(url=image)
    response_data = model.predict([image])
    predict_by_url = []
    for concept in response_data['outputs'][0]['data']['regions'][0]['data']['face']['identity']['concepts']:
        if concept['value']>0.95: 
            val = (concept['name'],concept['value'])
            predict_by_url.append(val)
        else:
            pass

    return predict_by_url



