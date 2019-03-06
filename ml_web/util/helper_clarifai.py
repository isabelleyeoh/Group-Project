from clarifai.rest import ClarifaiApp
import app


app_clarifai = ClarifaiApp(api_key=app.config['CLARIFAI_API_KEY'])

def get_relevant_tags(image_url):
    response_data = app_clarifai.tag_urls([image_url])

    tag_urls = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tag_urls.append(concept['name'])

    return tag_urls