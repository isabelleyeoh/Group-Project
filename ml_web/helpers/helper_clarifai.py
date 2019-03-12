from clarifai.rest import ClarifaiApp, Workflow
from app import app
import os
from clarifai.rest import Image as ClImage
from flask import render_template, redirect, url_for


app_clarifai=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])
app_clarifai_search=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY_SEARCH'])

# Clarifai - predict model
def model_prediction(image_path, model,input_file, workflow_id):

    # Add workflow
    workflow=Workflow(app_clarifai.api, workflow_id=workflow_id)
    # Predict using clarifai
    response_data = workflow.predict_by_url(url=image_path)

    result_cust_model=[]
    result_gen_model = []
    ref_list=['chair','table','sofa','armchair', 'lamp', 'bookcase','shelf']

    # Custom Model: Append results and return a list
    for concept in response_data['results'][0]['outputs'][1]['data']['concepts']:
        if concept['value']>0: 
            val = (concept['name'],concept['value'])
            result_cust_model.append(val)
        else:
            pass

    # General Model:

    for concept in response_data['results'][0]['outputs'][0]['data']['concepts']:
        if concept['value']>0.60 and concept['name']in ref_list:

            val = (concept['name'],concept['value'])
            result_gen_model.append(val)
        else:
            pass

    return result_cust_model, result_gen_model




