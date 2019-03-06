import app
from clarifai.rest import ClarifaiApp

app_clarifai = ClarifaiApp(api_key='0392301fc5b540f7aa868e5b1cf82c16')


def get_relevant_tags(image_url):
    general_model = app_clarifai.public_models.general_model
    response_data = general_model.predict_by_url(url=image_url)

    predict_by_url = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        predict_by_url.append(concept['name'])

    return predict_by_url