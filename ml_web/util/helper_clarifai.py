from clarifai.rest import ClarifaiApp
from app import app
import os


app_clarifai=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])

def get_relevant_tags(image_url):

    general_model = app_clarifai.public_models.general_model
    response_data = general_model.predict_by_url(url=image_url)

    predict_by_url = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        predict_by_url.append(concept['name'])

    return predict_by_url