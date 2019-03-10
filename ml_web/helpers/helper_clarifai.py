from clarifai.rest import ClarifaiApp, Workflow
from app import app
import os
from clarifai.rest import Image as ClImage
from flask import render_template, redirect, url_for


app_clarifai=ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])


# Clarifai - predict model
def model_prediction(image_path, model,input_file, workflow_id):

    # Add workflow
    workflow=Workflow(app_clarifai.api, workflow_id=workflow_id)
    # Use either filename or URL
    if input_file==True:
        image = app_clarifai.inputs.create_image_from_filename(filename=image_path)
    else:
        image = app_clarifai.inputs.create_image_from_url(url=image_path)
    #JSON response 
    response_data = workflow.predict([image])

    result_cust_model=[]
    result_gen_model = []

    for concept in response_data['results'][0]['outputs'][1]['data']['concepts']:
        if concept['value']>0: 
            val = (concept['name'],concept['value'])
            result_cust_model.append(val)
        else:
            pass
    
    # for concept in response_data['results'][0]['outputs'][0]['data']['concepts']:
    #     if concept['value']>0.90: 
    #         val = (concept['name'],concept['value'])
    #         result_gen_model.append(val)
    #     else:
    #         pass
    
    breakpoint()

    return result_cust_model




