import os
import config
from flask import Flask
from models.base_model import db
from clarifai.rest import ClarifaiApp


# Clarifai
from clarifai.rest import ClarifaiApp

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'ml_web')

app = Flask('MACHINE LEARNING', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

app_clarifai = ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])

general_model = app_clarifai.public_models.general_model


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

 

@app.route('/')
def index():
    image_url = "https://images.pexels.com/photos/912110/pexels-photo-912110.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
    print('\n'.join(get_relevant_tags(image_url))) 
    return "Pass"

# test machine learning API



def get_relevant_tags(image_url):
    response_data = app_clarifai.tag_urls([image_url])

    tag_urls = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tag_urls.append(concept['name'])

    return tag_urls



# model = app.public_models.general_model
# response = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
