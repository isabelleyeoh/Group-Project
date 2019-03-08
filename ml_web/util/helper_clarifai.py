from clarifai.rest import ClarifaiApp
from app import app
import os
from clarifai.rest import Image as ClImage
from flask import render_template, redirect, url_for

app_clarifai=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])

# Clarifai - get relevant image tags based on specified Clarifai model
def predict_image_bedframe(image, model):

    model = app_clarifai.models.get(model)
    image = ClImage(url=image)

    response_data = model.predict([image])
    # breakpoint()
    predict_by_url = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        if concept['value']>0.9: 
            val = (concept['name'],concept['value'])
            predict_by_url.append(val)
        else:
            pass

    return predict_by_url

# Clarifai - predict chair
def predict_model_chair(image_path, model,input_file):

    model = app_clarifai.models.get(model)

    if input_file==True:
        image = app_clarifai.inputs.create_image_from_filename(filename=image_path)
    else:
        image = app_clarifai.inputs.create_image_from_url(url=image_path)
        
    response_data = model.predict([image])
    predict_by_url = []

    for concept in response_data['outputs'][0]['data']['concepts']:
        if concept['value']>0: 
            val = (concept['name'],concept['value'])
            predict_by_url.append(val)
        else:
            pass

    return predict_by_url




